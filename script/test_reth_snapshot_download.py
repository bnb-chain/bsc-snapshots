"""Optional command integration tests: set RETH_BSC_BIN to a bundle-capable binary."""

import argparse
import functools
import http.server
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import threading
import unittest

import reth_snapshot_manifest as publisher


@unittest.skipUnless(os.environ.get("RETH_BSC_BIN"), "set RETH_BSC_BIN for command integration tests")
class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.requests = []
        requests = self.requests

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                requests.append(self.path)
                super().do_GET()

        self.server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(Handler, directory=str(self.root)),
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.base = f"http://127.0.0.1:{self.server.server_port}/"
        # These bytes test packaging/integrity only, not production database compatibility.
        self.files = {"db/mdbx.dat": b"source database and checkpoints",
                      "rocksdb/CURRENT": b"source index state",
                      "static_files/static_file_headers_0_499999": b"source headers",
                      "reth.toml": b"source pruning configuration",
                      "blobstore/sidecar": b"source sidecar",
                      "parlia_snapshots/mdbx.dat": b"source consensus snapshot"}
        contents = io.BytesIO()
        with tarfile.open(fileobj=contents, mode="w") as archive:
            for path, data in self.files.items():
                entry = tarfile.TarInfo(path)
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
        self.archive = self.root / "existing.tar.zst"
        # Match the large zstd window permitted by the production extraction instructions.
        compressed = subprocess.run(["zstd", "--compress", "--stdout", "--quiet", "--long=31"],
                                    input=contents.getvalue(), capture_output=True, check=True).stdout
        self.archive.write_bytes(compressed)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def manifest(self, chain_id, profile):
        args = argparse.Namespace(archive=None, bundle=self.archive, profile=profile,
                                  output=self.root / f"{chain_id}-{profile}-manifest.json",
                                  chain_id=chain_id, block=123, reth_version="integration-fixture",
                                  timestamp=123456, base_url=self.base)
        publisher.write_manifest(args.output, publisher.generate_manifest(args))
        return self.base + args.output.name

    def download(self, chain, url, target, *flags, binary=None):
        return subprocess.run([binary or os.environ["RETH_BSC_BIN"], "download", "--chain", chain,
                               "--manifest-url", url, "--datadir", str(target),
                               "--non-interactive", "--retry-backoff", "1ms", *flags],
                              capture_output=True, text=True, timeout=60)

    def test_both_profiles_on_both_networks_restore_and_reuse_unchanged_archives(self):
        original = self.archive.read_bytes()
        for chain_id, chain in [(56, "bsc"), (97, "bsc-testnet")]:
            for profile in ("full", "archive"):
                with self.subTest(chain=chain, profile=profile):
                    url = self.manifest(chain_id, profile)
                    target = self.root / f"restore-{chain_id}-{profile}"
                    plan = self.download(chain, url, target, f"--{profile}", "--print-plan-json")
                    self.assertEqual(plan.returncode, 0, plan.stdout + plan.stderr)
                    data = json.loads(plan.stdout[plan.stdout.index("{"):])
                    self.assertEqual(data["chainId"], chain_id)
                    self.assertEqual(len(data["archives"]), 1)
                    self.assertEqual(data["archives"][0]["component"], "bundle")
                    self.assertFalse(target.exists())
                    result = self.download(chain, url, target, f"--{profile}")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    for path, contents in self.files.items():
                        self.assertEqual((target / path).read_bytes(), contents)
                    count = self.requests.count("/existing.tar.zst")
                    rerun = self.download(chain, url, target)
                    self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
                    self.assertEqual(self.requests.count("/existing.tar.zst"), count)
                    (target / "db/mdbx.dat").write_bytes(b"damaged")
                    repair = self.download(chain, url, target)
                    self.assertEqual(repair.returncode, 0, repair.stdout + repair.stderr)
                    self.assertGreater(self.requests.count("/existing.tar.zst"), count)
                    self.assertEqual((target / "db/mdbx.dat").read_bytes(), self.files["db/mdbx.dat"])
        self.assertEqual(self.archive.read_bytes(), original)

    def test_wrong_network_and_profile_fail_before_force_modifies_destination(self):
        url = self.manifest(97, "full")
        target = self.root / "existing-data"
        (target / "db").mkdir(parents=True)
        sentinel = target / "db/mdbx.dat"
        sentinel.write_bytes(b"keep")
        for chain, flags, error in [
            ("bsc", [], "Snapshot chain ID 97 does not match selected chain ID 56"),
            ("bsc-testnet", ["--archive"], "--archive requires an archive bundle"),
            ("bsc-testnet", ["--minimal"], "Complete snapshot bundles do not support"),
        ]:
            result = self.download(chain, url, target, "--force", *flags)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(error, result.stdout + result.stderr)
            self.assertEqual(sentinel.read_bytes(), b"keep")
        self.assertNotIn("/existing.tar.zst", self.requests)
        if legacy := os.environ.get("RETH_BSC_LEGACY_BIN"):
            result = self.download("bsc-testnet", url, target, "--force", binary=legacy)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing field `components`", result.stdout + result.stderr)
            self.assertEqual(sentinel.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
