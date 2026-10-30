import argparse
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import reth_snapshot_manifest as publisher


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def archive(self, name, members):
        contents = io.BytesIO()
        with tarfile.open(fileobj=contents, mode="w") as archive:
            for member, data in members:
                if isinstance(member, str):
                    member = tarfile.TarInfo(member)
                    member.size = len(data)
                archive.addfile(member, io.BytesIO(data) if member.isfile() else None)
        path = self.root / name
        compressed = subprocess.run(
            ["zstd", "--compress", "--stdout", "--quiet"],
            input=contents.getvalue(), capture_output=True, check=True,
        ).stdout
        path.write_bytes(compressed)
        return path

    def inputs(self):
        archives = []
        for component, (root, segment) in publisher.COMPONENTS.items():
            filename = f"static_file_{segment}_0_499999" if segment else "data"
            path = self.archive(f"existing-{component}.tar.zst", [(f"./{root}/{filename}", b"abc")])
            archives.append((component, path))
        return argparse.Namespace(
            archive=archives, output=self.root / "manifest.json", chain_id=56, block=123,
            reth_version="test-producer", timestamp=123456, base_url="https://example.com/snapshot",
        )

    def test_eight_existing_archives_have_exact_output_checksums_and_are_unchanged(self):
        args = self.inputs()
        original = {path: path.read_bytes() for _, path in args.archive}
        manifest = publisher.generate_manifest(args)
        publisher.write_manifest(args.output, manifest)
        self.assertEqual(manifest, json.loads(args.output.read_text()))
        self.assertEqual(manifest["chain_id"], 56)
        self.assertEqual(manifest["block"], 123)
        self.assertEqual(manifest["storage_version"], 2)
        self.assertEqual(manifest["timestamp"], 123456)
        self.assertEqual(manifest["base_url"], "https://example.com/snapshot/")
        self.assertEqual(set(manifest["components"]), set(publisher.COMPONENTS))
        for component, path in args.archive:
            entry = manifest["components"][component]
            self.assertEqual(entry["file"], path.name)
            self.assertEqual(entry["size"], len(original[path]))
            self.assertEqual(entry["decompressed_size"], 3)
            self.assertEqual(entry["output_files"][0]["blake3"],
                             "6437b3ac38465133ffb63b75273a8db548c558465d79db03fd359c6cd5bd9d85")
            self.assertFalse(entry["output_files"][0]["path"].startswith("./"))
            self.assertEqual(path.read_bytes(), original[path])
        # No extracted databases or static files were created by the publisher.
        self.assertEqual({path.name for path in self.root.iterdir()},
                         {path.name for path in original} | {"manifest.json"})

    def test_missing_or_duplicate_components_fail_before_scanning(self):
        args = self.inputs()
        with patch.object(publisher, "inspect_archive") as inspect:
            args.archive = args.archive[:-1]
            with self.assertRaisesRegex(ValueError, "missing archive components"):
                publisher.generate_manifest(args)
            args.archive.append(args.archive[0])
            with self.assertRaisesRegex(ValueError, "exactly once"):
                publisher.generate_manifest(args)
            inspect.assert_not_called()

    def test_invalid_tar_paths_links_and_wrong_components_are_rejected(self):
        for name in ["../db/data", "/db/data", "db/../outside", "db\\data", "jwt.hex"]:
            with self.subTest(name=name):
                path = self.archive("bad.tar.zst", [(name, b"abc")])
                with self.assertRaises(ValueError):
                    publisher.inspect_archive("state", path)
        for linktype in [tarfile.SYMTYPE, tarfile.LNKTYPE]:
            with self.subTest(linktype=linktype):
                member = tarfile.TarInfo("db/link")
                member.type = linktype
                member.linkname = "../../outside"
                path = self.archive("link.tar.zst", [(member, b"")])
                with self.assertRaisesRegex(ValueError, "only regular files"):
                    publisher.inspect_archive("state", path)
        path = self.archive("wrong.tar.zst", [("static_files/static_file_receipts_0_499999", b"a")])
        with self.assertRaisesRegex(ValueError, "unexpected file in headers"):
            publisher.inspect_archive("headers", path)

    def test_duplicate_normalized_outputs_and_empty_archives_are_rejected(self):
        path = self.archive("duplicate.tar.zst", [("db/data", b"a"), ("./db/data", b"b")])
        with self.assertRaisesRegex(ValueError, "duplicate output file"):
            publisher.inspect_archive("state", path)
        path = self.archive("empty.tar.zst", [])
        with self.assertRaisesRegex(ValueError, "contains no files"):
            publisher.inspect_archive("state", path)

    def test_truncated_compression_does_not_publish_manifest(self):
        args = self.inputs()
        path = args.archive[-1][1]
        path.write_bytes(path.read_bytes()[:-4])
        with self.assertRaises((ValueError, tarfile.TarError)):
            publisher.generate_manifest(args)
        self.assertFalse(args.output.exists())

    def test_archive_changed_after_scan_does_not_publish_manifest(self):
        args = self.inputs()
        inspect = publisher.inspect_archive
        def modify_previous(component, path):
            result = inspect(component, path)
            if component == args.archive[-1][0]:
                with args.archive[0][1].open("ab") as previous:
                    previous.write(b"modified")
            return result
        with patch.object(publisher, "inspect_archive", side_effect=modify_previous):
            with self.assertRaisesRegex(ValueError, "archive changed"):
                publisher.generate_manifest(args)
        self.assertFalse(args.output.exists())

    def test_existing_manifest_is_preserved_even_if_created_after_validation(self):
        output = self.root / "manifest.json"
        output.write_text("published")
        with self.assertRaises(FileExistsError):
            publisher.write_manifest(output, {"new": True})
        self.assertEqual(output.read_text(), "published")
        self.assertEqual(list(self.root.iterdir()), [output])

    def test_directory_members_and_empty_regular_files(self):
        directory = tarfile.TarInfo("./db/")
        directory.type = tarfile.DIRTYPE
        path = self.archive("dirs.tar.zst", [(directory, b""), ("db/empty", b"")])
        result = publisher.inspect_archive("state", path)
        self.assertEqual(result["decompressed_size"], 0)
        self.assertEqual(result["output_files"], [{
            "path": "db/empty", "size": 0,
            "blake3": "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262",
        }])

    def test_cli_rejects_bad_metadata_without_creating_output(self):
        result = subprocess.run(
            [sys.executable, str(Path(publisher.__file__)), "--chain-id", "56", "--block", "-1",
             "--reth-version", "test", "--base-url", "https://example.com", "--output",
             str(self.root / "manifest.json"), "--archive", "state=missing.tar.zst"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsigned 64-bit integer", result.stderr)
        self.assertFalse((self.root / "manifest.json").exists())

    def test_base_url_rejects_credentials_query_and_non_directory_schemes(self):
        for url in ["s3://bucket", "https://user:password@example.com", "https://example.com?a=1",
                    "https://example.com#fragment", "file://remote/path", "relative/path"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                publisher.validate_base_url(url)
        self.assertEqual(publisher.validate_base_url("file:///tmp/snapshot"), "file:///tmp/snapshot/")


if __name__ == "__main__":
    unittest.main()
