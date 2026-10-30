# Publishing manifests for existing Reth archive snapshots

The eight-file mainnet archive snapshot can be published through a Reth download
manifest without changing its `.tar.zst` files. The manifest is a packing list:
it names each archive and records the size and BLAKE3 checksum of every file that
the downloader will extract.

This workflow supports the **eight-component archive profile**. Single-file full,
FastNode, and testnet snapshots continue to use their existing download workflow.
Do not label a pruned snapshot as an archive snapshot, or map a whole multi-directory
snapshot to the `state` component.

## Generate the manifest

Requirements: Python 3.10 or newer, `zstd`, and the Python `blake3` package:

```sh
python3 -m venv .venv
.venv/bin/pip install -r script/reth-manifest-requirements.txt
```

Use the completed, immutable archives from **one consistent snapshot of the node**.
The script cannot verify database consistency or infer the snapshot's actual head
from archive names. Record the chain ID, head block, and producer version when
making the snapshot. Chain IDs are 56 for mainnet and 97 for testnet.

Example for the existing mainnet naming convention (set the two metadata values
from the actual snapshot, not from the current live node):

```sh
archive_dir=/srv/snapshots
snapshot_name=20261002_mainnet_reth_mdbx
public_base_url=https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev
manifest_path="$archive_dir/20261002-mainnet-reth-archive-manifest.json"

: "${SNAPSHOT_BLOCK:?Set the actual snapshot head block}"
: "${RETH_VERSION:?Set the producer Reth-BSC version and commit}"

.venv/bin/python script/reth_snapshot_manifest.py \
  --chain-id 56 --block "$SNAPSHOT_BLOCK" --reth-version "$RETH_VERSION" \
  --base-url "$public_base_url" --output "$manifest_path" \
  --archive "state=$archive_dir/${snapshot_name}_db_archive_node_v2.tar.zst" \
  --archive "rocksdb_indices=$archive_dir/${snapshot_name}_rocksdb_archive_node_v2.tar.zst" \
  --archive "headers=$archive_dir/${snapshot_name}_static_files_headers_archive_node_v2.tar.zst" \
  --archive "transactions=$archive_dir/${snapshot_name}_static_files_transactions_archive_node_v2.tar.zst" \
  --archive "transaction_senders=$archive_dir/${snapshot_name}_static_files_transaction-senders_archive_node_v2.tar.zst" \
  --archive "receipts=$archive_dir/${snapshot_name}_static_files_receipts_archive_node_v2.tar.zst" \
  --archive "account_changesets=$archive_dir/${snapshot_name}_static_files_account-change-sets_archive_node_v2.tar.zst" \
  --archive "storage_changesets=$archive_dir/${snapshot_name}_static_files_storage-change-sets_archive_node_v2.tar.zst"
```

The tool streams through each archive once and hashes the decompressed file
contents. It does not extract a second copy to disk, recompress, rename, upload,
or change the archives. Scanning several terabytes still takes substantial I/O
and CPU time. Zstd windows up to `--long=31` are allowed, matching the existing
extraction instructions; decompression can therefore require substantial RAM.

All eight components are required. Entries must be regular files rooted at `db/`,
`rocksdb/`, or the corresponding `static_files/static_file_<segment>_...` paths.
The tool rejects links, unsafe paths, duplicate output files, changed input
archives, and incomplete compressed streams. It writes the manifest only after
all archives succeed and refuses to overwrite an existing manifest.

## Upload and validate

1. Upload the eight archives using the existing upload process. Preserve their
   basenames and place them together at the public `--base-url`. Already published
   archives can be reused if the local files are exactly the same immutable files.
2. Verify that each public archive URL is accessible, then upload the manifest
   **last**. Keep its name versioned; do not overwrite an older snapshot's files.
   For an R2/S3 upload using your existing credentials and endpoint, for example:

   ```sh
   aws s3 cp "$manifest_path" \
     "s3://$SNAPSHOT_BUCKET/20261002-mainnet-reth-archive-manifest.json" \
     --endpoint-url "$R2_ENDPOINT" --content-type application/json
   ```

3. With the Reth-BSC release that will consume this snapshot, inspect the plan:

   ```sh
   reth-bsc download --chain bsc --archive \
     --manifest-url "$public_base_url/20261002-mainnet-reth-archive-manifest.json" \
     --datadir /srv/reth-restore --print-plan-json
   ```

4. Restore into a fresh directory by removing `--print-plan-json`. For the published
   mainnet archive, also supply the documented database options
   `--db.max-size=12TB --db.page-size=8KB`. Check those options against the actual
   snapshot if its database layout changes.
5. Start the restored node with the matching chain, database, and static-file
   configuration. Compare its snapshot head/hash, state queries, historical
   receipts, and ability to catch up. Verify Parlia data and the required recent
   blob-sidecar availability separately; a manifest does not supply files absent
   from the eight input archives.
6. Add the validated manifest URL and supported client version to the snapshot
   table in this repository.

## Compatibility and disk space

The manifest uses Reth's storage-v2 schema and eight `Single` component entries.
This shape and the required per-output-file checksums were checked against
`bnb-chain/reth` revision `2b6198f7dd8533cc9c8f5fd5113b8b16b2fddb67` in the Reth-BSC
upgrade stack. This does not establish compatibility of every currently published
production database with that client. Validate a complete restore before
advertising a new supported release.

For this revision, manifest downloads cache each archive before extraction. The
manifest path does **not** honor `--resumable=false`; that flag affects the direct
single-URL download path. Allow space for the restored files and concurrent cached
archives, and test the actual zstd window settings with the consuming client.
This publishing tool does not fix the downloader's disk-space behavior.

These are whole-component archives. Downloading a recent range still requires
the whole selected archive; `--full` or `--minimal` does not turn them into small
block-range chunks. Use `--archive` for this workflow. Future block-range packaging
can improve selective downloads without replacing the existing archive URLs.

## Tests

```sh
.venv/bin/python -m unittest discover -s script -p 'test_reth_snapshot_manifest.py' -v
```

Related request: [Support for reth download (#458)](https://github.com/bnb-chain/bsc-snapshots/issues/458).
