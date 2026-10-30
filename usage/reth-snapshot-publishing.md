# Publishing Reth snapshot manifests

Full-node and archive snapshots on **both mainnet and testnet** can use
`reth-bsc download --manifest-url` with the matching client support. Existing
`.tar.zst` files with the supported datadir-relative layout can be reused without
joining, splitting or recompressing them. Publish one extra JSON manifest for each
snapshot. Check the layout requirements below before backfilling older archives.

| Snapshot | Existing layout | Generator input |
| --- | --- | --- |
| Mainnet archive | Eight component archives | Eight `--archive COMPONENT=PATH` arguments |
| Mainnet full | One complete archive | `--bundle PATH --profile full` |
| Testnet archive | One complete archive | `--bundle PATH --profile archive` |
| Testnet full | One complete archive | `--bundle PATH --profile full` |

Complete archives require the bundle support in
[bnb-chain/reth #247](https://github.com/bnb-chain/reth/pull/247), enabled by
[Reth-BSC #598](https://github.com/bnb-chain/reth-bsc/pull/598). Older clients reject bundle manifests. The
component format remains compatible with the previously tested upgrade revision.
These changes are drafts pending production restore validation; they do not
establish compatibility of every published database with a new client release.
FastNode snapshots and their special startup settings are outside this workflow.

The manifest records the archive names, extracted-file sizes, and BLAKE3
checksums. Its profile describes the **source snapshot**: a full snapshot does
not become an archive snapshot by changing a label or a download flag.

## Automatic monthly publishing

The MDBX snapshot upload job generates manifests automatically. It records the
stopped-node checkpoint and producer version, scans each archive before uploading
and deleting its local copy, then publishes the manifest only after all archive
uploads and public size checks succeed. Mainnet archive still processes one
compressed part at a time. Failed runs do not advertise a partial snapshot.

Successful runs publish a dated manifest and update a stable path under the
public snapshot base URL:

| Network | Node | Manifest path |
| --- | --- | --- |
| Mainnet | Full | `manifests/mainnet/full/latest.json` |
| Mainnet | Archive | `manifests/mainnet/archive/latest.json` |
| Testnet | Full | `manifests/testnet/full/latest.json` |
| Testnet | Archive | `manifests/testnet/archive/latest.json` |

These paths are **pending deployment**, not currently published download links.
After the first production restore has been validated, add the stable URL and
supported client version to the README's **Manifest** column. Users then find
one link beside their snapshot and follow the [command instructions](./reth-bsc-snapshot.md#download-with-the-reth-command).

New uploader archives use datadir-relative paths. Some older upload jobs stored
parent directories inside the tar; those archives cannot be described by this
generator unchanged. Do not publish a manifest that strips those paths only in
JSON: the client would extract to the wrong directory. Existing remote files are
left untouched. The commands below apply to archives with the supported layout.

## Generate a manifest manually (backfill or other upload systems)

Requirements: Python 3.10 or newer, `zstd`, and the Python `blake3` package:

```sh
python3 -m venv .venv
.venv/bin/pip install -r script/reth-manifest-requirements.txt
```

Use the completed, immutable archives from **one consistent snapshot of the node**.
The script cannot verify database consistency or infer the snapshot's actual head
from archive names. Record the chain ID, head block, and producer version when
making the snapshot. Chain IDs are 56 for mainnet and 97 for testnet.

### Eight-file mainnet archive

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

### Single-file mainnet or testnet snapshot

For example, publish the current testnet full-node snapshot unchanged:

```sh
archive_dir=/srv/snapshots
public_base_url=https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev
manifest_path="$archive_dir/20261002-testnet-reth-full-manifest.json"

: "${SNAPSHOT_BLOCK:?Set the actual snapshot head block}"
: "${RETH_VERSION:?Set the producer Reth-BSC version and commit}"

.venv/bin/python script/reth_snapshot_manifest.py \
  --chain-id 97 --block "$SNAPSHOT_BLOCK" --reth-version "$RETH_VERSION" \
  --base-url "$public_base_url" --output "$manifest_path" \
  --profile full \
  --bundle "$archive_dir/20261002_testnet_reth_mdbx_full_node_v2.tar.zst"
```

For testnet archive, use `--profile archive` and its archive filename. For mainnet
full, use `--chain-id 56`, `--profile full`, and the mainnet full filename. Give
each resulting manifest its own network/profile/date name.

### Input checks and scan cost

The tool streams through each archive once and hashes the decompressed file
contents. It does not extract a second copy to disk, recompress, rename, upload,
or change the archives. Scanning several terabytes still takes substantial I/O
and CPU time. Zstd windows up to `--long=31` are allowed, matching the existing
extraction instructions; decompression can therefore require substantial RAM.

Component mode requires all eight archives and the archive profile. Its files
must be rooted at `db/`, `rocksdb/`, or the corresponding
`static_files/static_file_<segment>_...` paths. Bundle mode requires an explicit
profile and `db/mdbx.dat`; it accepts regular files under `db/`, `rocksdb/`, and
`static_files/`, `blobstore/`, and `parlia_snapshots/`, plus an optional top-level `reth.toml`. Archives must contain
relative paths directly under these directories, without an extra parent folder.
The tool rejects links, unsafe paths, duplicate output files, changed input
archives, and incomplete compressed streams. It writes the manifest only after
all archives succeed and refuses to overwrite an existing manifest.

## Upload and validate

1. Upload the archive or archives using the existing upload process. Preserve their
   basenames and place them together at the public `--base-url`. Already published
   archives can be reused if the local files are exactly the same immutable files.
2. Verify that each public archive URL is accessible, then upload the manifest
   **last**. Keep its name versioned; do not overwrite an older snapshot's files.
   For an R2/S3 upload using your existing credentials and endpoint, for example:

   ```sh
   aws s3 cp "$manifest_path" \
     "s3://$SNAPSHOT_BUCKET/$(basename "$manifest_path")" \
     --endpoint-url "$R2_ENDPOINT" --content-type application/json
   ```

3. With a Reth-BSC release supporting the manifest, inspect the plan. For the
   eight-file mainnet archive:

   ```sh
   reth-bsc download --chain bsc --archive \
     --manifest-url "$public_base_url/20261002-mainnet-reth-archive-manifest.json" \
     --datadir /srv/reth-restore --print-plan-json
   ```

   For a single-file snapshot, use its corresponding chain and manifest URL:

   ```sh
   reth-bsc download --chain bsc-testnet \
     --manifest-url "$public_base_url/20261002-testnet-reth-full-manifest.json" \
     --datadir /srv/reth-restore --print-plan-json
   ```

   Use `--chain bsc` for mainnet. A bundle automatically restores the complete
   snapshot; no component selection is needed. `--full` or `--archive` can assert
   the matching profile but cannot convert it. The client rejects wrong networks,
   mismatched profiles, and component/range selections for bundles.

4. Restore into a fresh directory by removing `--print-plan-json`. For the published
   mainnet archive, also supply the documented database options
   `--db.max-size=12TB --db.page-size=8KB`. Check those options against the actual
   snapshot if its database layout changes.
5. Start the restored node with the matching chain, database, and static-file
   configuration. Compare its snapshot head/hash, state queries, historical
   receipts, and ability to catch up. Verify Parlia data and the required recent
   blob-sidecar availability separately; a manifest does not supply files absent
   from its input archives. Bundles preserve database pruning/index checkpoints
   and included configuration. If `reth.toml` is absent, supply the source node's
   matching settings when starting the restored node; the downloader does not
   infer missing pruning settings.
6. Add the validated manifest URL and supported client version to the snapshot
   table in this repository.

## Compatibility and disk space

Component manifests use Reth's storage-v2 schema and eight `Single` component entries.
This shape and the required per-output-file checksums were checked against
`bnb-chain/reth` revision `2b6198f7dd8533cc9c8f5fd5113b8b16b2fddb67` in the Reth-BSC
upgrade stack. This does not establish compatibility of every currently published
production database with that client. Validate a complete restore before
advertising a new supported release.

Bundle manifests use a `bundle` object with `profile` and `archive` fields in
place of `components`. Do not add an empty `components` object: omitting it makes
older clients fail instead of processing a bundle as an empty modular snapshot.
The archive entry uses the same sizes and output checksums as component entries.

Manifest downloads, including bundles, cache each archive before extraction. The
manifest path does **not** honor `--resumable=false`; that flag affects the direct
single-URL download path. Allow space for the restored files and concurrent cached
archives. The companion client accepts zstd windows up to `--long=31`; large
windows can require up to 2 GiB of decoder memory per concurrent archive.
This publishing tool does not fix the downloader's disk-space behavior.

The eight component files are whole-component archives. Downloading a recent range still requires
the whole selected archive; `--full` or `--minimal` does not turn them into small
block-range chunks. Use `--archive` for this workflow. Future block-range packaging
can improve selective downloads without replacing the existing archive URLs.
Complete bundles always download the whole snapshot, and preserve its source
profile. They reject `--minimal`, component/range flags, `--without-rocksdb`, and
`--prune-unlisted`. Use a fresh directory for another snapshot, or explicitly
clear previous snapshot data with the client's `--force` option.

## Tests

```sh
.venv/bin/python -m unittest discover -s script -p 'test_reth_snapshot_manifest.py' -v
```

The command integration tests use small HTTP fixtures for both profiles and both
network IDs. They verify exact restored bytes, reuse, repair, large zstd windows,
and rejection before `--force` modifies a destination. They do not validate
production databases:

```sh
RETH_BSC_BIN=/path/to/bundle-capable/reth-bsc \
  .venv/bin/python -m unittest discover -s script -p 'test_reth_snapshot_download.py' -v
```

Related request: [Support for reth download (#458)](https://github.com/bnb-chain/bsc-snapshots/issues/458).
