#!/usr/bin/env python3
"""Describe existing Reth component archives without extracting or repacking them."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.parse import urlsplit

import blake3


# These are the component keys understood by Reth's modular downloader.
COMPONENTS = {
    "state": ("db", None),
    "rocksdb_indices": ("rocksdb", None),
    "headers": ("static_files", "headers"),
    "transactions": ("static_files", "transactions"),
    "transaction_senders": ("static_files", "transaction-senders"),
    "receipts": ("static_files", "receipts"),
    "account_changesets": ("static_files", "account-change-sets"),
    "storage_changesets": ("static_files", "storage-change-sets"),
}
READ_SIZE = 4 * 1024 * 1024


def archive_argument(value):
    component, separator, filename = value.partition("=")
    if not separator or component not in COMPONENTS or not filename:
        raise argparse.ArgumentTypeError(
            "expected COMPONENT=PATH; components: " + ", ".join(COMPONENTS)
        )
    return component, Path(filename)


def unsigned_integer(value):
    number = int(value)
    if not 0 <= number < 2**64:
        raise argparse.ArgumentTypeError("expected an unsigned 64-bit integer")
    return number


def validate_archives(archives, output):
    """Validate all inputs before scanning potentially multi-terabyte archives."""
    components = [component for component, _ in archives]
    if len(set(components)) != len(components):
        raise ValueError("each component must be supplied exactly once")
    missing = set(COMPONENTS) - set(components)
    if missing:
        raise ValueError("missing archive components: " + ", ".join(sorted(missing)))
    filenames = set()
    for _, path in archives:
        if not path.is_file() or not path.name.endswith(".tar.zst"):
            raise ValueError(f"expected an existing .tar.zst file: {path}")
        # Names are joined to base_url by the consumer; URL syntax must not change them.
        if any(char in path.name for char in "%?#\\"):
            raise ValueError(f"archive filename contains URL-special characters: {path.name}")
        if path.name in filenames:
            raise ValueError(f"archive filenames must be unique: {path.name}")
        filenames.add(path.name)
    if output.exists():
        raise ValueError(f"output already exists; choose a new manifest path: {output}")


def validate_base_url(value):
    parsed = urlsplit(value)
    if (
        parsed.scheme not in ("https", "http", "file")
        or (parsed.scheme != "file" and not parsed.netloc)
        or (parsed.scheme == "file" and (parsed.netloc or not parsed.path.startswith("/")))
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError("base URL must be an HTTP(S) directory or absolute file:/// directory")
    return value.rstrip("/") + "/"


def member_path(member, component):
    path = PurePosixPath(member.name)
    if path.is_absolute() or ".." in path.parts or "\\" in member.name:
        raise ValueError(f"unsafe archive path: {member.name}")
    root, segment = COMPONENTS[component]
    if member.isdir() and (not path.parts or path.parts[0] == root):
        return None
    if not member.isfile():
        raise ValueError(f"only regular files and directories are supported: {member.name}")
    if len(path.parts) < 2 or path.parts[0] != root:
        raise ValueError(f"{component} files must be rooted at {root}/: {member.name}")
    if segment and (
        len(path.parts) != 2 or not path.name.startswith(f"static_file_{segment}_")
    ):
        raise ValueError(f"unexpected file in {component}: {member.name}")
    return path.as_posix()


def file_identity(path):
    stat = path.stat()
    return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def inspect_archive(component, path):
    """Hash logical file contents in one decompression pass, with bounded buffers."""
    before = file_identity(path)
    files = {}
    # The published snapshots use --long=31. Keep diagnostics out of the data stream
    # and avoid a pipe filling while tarfile is consuming stdout.
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen(
            ["zstd", "--decompress", "--stdout", "--long=31", "--", str(path)],
            stdout=subprocess.PIPE,
            stderr=errors,
        )
        try:
            with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
                for member in archive:
                    relative = member_path(member, component)
                    if relative is None:
                        continue
                    if relative in files:
                        raise ValueError(f"duplicate output file: {relative}")
                    digest = blake3.blake3()
                    size = 0
                    with archive.extractfile(member) as contents:
                        while chunk := contents.read(READ_SIZE):
                            digest.update(chunk)
                            size += len(chunk)
                    if size != member.size:
                        raise ValueError(f"truncated archive member: {relative}")
                    files[relative] = {
                        "path": relative,
                        "size": size,
                        "blake3": digest.hexdigest(),
                    }
            # Consume the end of the compressed stream so zstd validates its checksum.
            while process.stdout.read(READ_SIZE):
                pass
            returncode = process.wait()
            if returncode:
                errors.seek(0)
                detail = errors.read(8192).decode(errors="replace").strip()
                raise ValueError(f"zstd failed for {path.name}: {detail}")
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    if file_identity(path) != before:
        raise ValueError(f"archive changed while being scanned: {path}")
    if not files:
        raise ValueError(f"archive contains no files: {path}")
    return {
        "file": path.name,
        "size": before[2],
        "decompressed_size": sum(item["size"] for item in files.values()),
        "output_files": [files[name] for name in sorted(files)],
    }


def generate_manifest(args):
    validate_archives(args.archive, args.output)
    base_url = validate_base_url(args.base_url)
    if shutil.which("zstd") is None:
        raise ValueError("zstd is required; install it before generating a manifest")
    identities = {path: file_identity(path) for _, path in args.archive}
    components = {}
    outputs = set()
    for component, path in args.archive:
        print(f"Scanning {component}: {path}", file=sys.stderr, flush=True)
        entry = inspect_archive(component, path)
        for item in entry["output_files"]:
            if item["path"] in outputs:
                raise ValueError(f"output appears in multiple archives: {item['path']}")
            outputs.add(item["path"])
        components[component] = entry
    # Catch archives replaced after their own scan but before the manifest is complete.
    for path, identity in identities.items():
        if file_identity(path) != identity:
            raise ValueError(f"archive changed while generating the manifest: {path}")
    return {
        "block": args.block,
        "chain_id": args.chain_id,
        "storage_version": 2,
        "timestamp": args.timestamp if args.timestamp is not None else int(time.time()),
        "base_url": base_url,
        "reth_version": args.reth_version,
        "components": components,
    }


def write_manifest(path, manifest):
    """Publish a complete file without overwriting an existing manifest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            json.dump(manifest, temporary, indent=2)
            temporary.write("\n")
            temporary.flush()
            os.fchmod(temporary.fileno(), 0o644)
            os.fsync(temporary.fileno())
            # An atomic link fails if another writer has already published this path.
            os.link(temporary_path, path)
        finally:
            temporary_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chain-id", required=True, type=unsigned_integer)
    parser.add_argument("--block", required=True, type=unsigned_integer,
                        help="actual snapshot head, not the last static-file range endpoint")
    parser.add_argument("--reth-version", required=True, help="producer's Reth-BSC version/commit")
    parser.add_argument("--timestamp", type=unsigned_integer, help="Unix timestamp; defaults to now")
    parser.add_argument("--base-url", required=True, help="public directory containing the archives")
    parser.add_argument("--output", required=True, type=Path, help="new manifest.json path")
    parser.add_argument("--archive", action="append", required=True, type=archive_argument,
                        metavar="COMPONENT=PATH", help="repeat once for each of the eight components")
    args = parser.parse_args()
    try:
        manifest = generate_manifest(args)
        write_manifest(args.output, manifest)
    except (OSError, ValueError, tarfile.TarError, subprocess.SubprocessError) as error:
        parser.exit(1, f"error: {error}\n")
    print(f"Wrote {args.output} ({len(manifest['components'])} components)")


if __name__ == "__main__":
    main()
