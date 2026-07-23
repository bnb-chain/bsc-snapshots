
# About BSC Snapshots
Currently, there are 3 sources of BSC snapshot could be used, if you are unclear about their differences, you may refer [Clarification of the snapshots](https://github.com/bnb-chain/bsc-snapshots/issues/349) first, to decide which snapshot suit you the most.

## Source-1: Legacy Full Node
Usage: [usage/legacyfullnode_usage.md](./usage/legacyfullnode_usage.md)

> Currently, snapshots are provided as block history data divided by year. Each list includes world states, historical block files, URL, MD5, file size. Users can use the provided tools to quickly download.

> The Pruned Snapshot is better for internal/private nodes, it only keeps the latest 9w historical blocks and requires BSC client >=[v1.5.5](https://github.com/bnb-chain/bsc/releases/tag/v1.5.5).

### mainnet(monthly update)

| Snapshot Type   | Snapshot File                                                                               | Total Size | Remark        |
|-----------------|---------------------------------------------------------------------------------------------|------------|---------------|
| Full Snapshot   | [mainnet-geth-pbss-20260525](dist/mainnet-geth-pbss-20260525.csv)                           | **~6.0TB** | BSC >= v1.7.2 |
| Pruned Snapshot | [mainnet-geth-pbss-20260525-pruneancient](dist/mainnet-geth-pbss-20260525-pruneancient.csv) | **~1.6TB** | BSC >= v1.7.2 |

### testnet(update every 4 months)

| Snapshot Type   | Snapshot File                                                                               | Total Size | Remark        |
|-----------------|---------------------------------------------------------------------------------------------|------------|---------------|
| Full Snapshot   | [testnet-geth-pbss-20260407](dist/testnet-geth-pbss-20260407.csv)                           | **~440GB** | BSC >= v1.7.2 |
| Pruned Snapshot | [testnet-geth-pbss-20260407-pruneancient](dist/testnet-geth-pbss-20260407-pruneancient.csv) | **~180GB** | BSC >= v1.7.2 |

### Download

You can download the mainnet or testnet files separately in the list and unzip them in a same directory. Or you can use the following script:

```bash
# install aria2 on your os
yum install aria2
wget https://raw.githubusercontent.com/bnb-chain/bsc-snapshots/main/dist/fetch-snapshot.sh
```

**Parameters:**
- `-d` download, `-e` extract, `-c` verify MD5 checksum, `-p` use pruned snapshot
- `-D <dir>` directory to store downloaded archives
- `-E <dir>` extraction target, should be the node's `--datadir` (e.g. `/data/bsc`), files will be extracted to `<dir>/geth/chaindata/...`
- `--auto-delete` delete each archive immediately after extraction to save disk space
- `-p` auto-appends `-pruneancient` to the snapshot name, do **NOT** use with a name that already has the suffix

**Quick start (download, verify, extract, auto-delete in one step):**

```bash
# full snapshot (~6.0TB, needs at least 7TB free, or 6TB with --auto-delete)
bash fetch-snapshot.sh -d -e -c --auto-delete -D /data/snapshot -E /data/bsc mainnet-geth-pbss-20260525

# pruned snapshot (~1.6TB, needs at least 2TB free with --auto-delete)
bash fetch-snapshot.sh -d -e -c -p --auto-delete -D /data/snapshot -E /data/bsc mainnet-geth-pbss-20260525
```

After extraction, files will be at `/data/bsc/geth/chaindata/...`, start geth with `--datadir /data/bsc`.

**Step by step (download first, extract later):**

```bash
# step 1: download & checksum
bash fetch-snapshot.sh -d -c -D /data/snapshot mainnet-geth-pbss-20260525

# step 2: extract to datadir
bash fetch-snapshot.sh -e -D /data/snapshot -E /data/bsc mainnet-geth-pbss-20260525
```

You can remove the `-c` option to skip MD5 checking. Run `bash fetch-snapshot.sh --help` for all options.

> Please keep `fetch-snapshot.sh` the latest version.

### Previous snapshot

- **mainnet**:
  - [mainnet-geth-pbss-20260408](dist/mainnet-geth-pbss-20260408.csv), [mainnet-geth-pbss-20260408-pruneancient](dist/mainnet-geth-pbss-20260408-pruneancient.csv)
  - [mainnet-geth-pbss-20260306](dist/mainnet-geth-pbss-20260306.csv), [mainnet-geth-pbss-20260306-pruneancient](dist/mainnet-geth-pbss-20260306-pruneancient.csv)
  - [mainnet-geth-pbss-20260202](dist/mainnet-geth-pbss-20260202.csv), [mainnet-geth-pbss-20260202-pruneancient](dist/mainnet-geth-pbss-20260202-pruneancient.csv)
  - [mainnet-geth-pbss-20260104](dist/mainnet-geth-pbss-20260104.csv), [mainnet-geth-pbss-20260104-pruneancient](dist/mainnet-geth-pbss-20260104-pruneancient.csv)
  - [mainnet-geth-pbss-20251205](dist/mainnet-geth-pbss-20251205.csv), [mainnet-geth-pbss-20251205-pruneancient](dist/mainnet-geth-pbss-20251205-pruneancient.csv)
  - [mainnet-geth-pbss-20251114](dist/mainnet-geth-pbss-20251114.csv), [mainnet-geth-pbss-20251114-pruneancient](dist/mainnet-geth-pbss-20251114-pruneancient.csv)
  - [mainnet-geth-pbss-20251013](dist/mainnet-geth-pbss-20251013.csv), [mainnet-geth-pbss-20251013-pruneancient](dist/mainnet-geth-pbss-20251013-pruneancient.csv)
  - [mainnet-geth-pbss-20250906](dist/mainnet-geth-pbss-20250906.csv), [mainnet-geth-pbss-20250906-pruneancient](dist/mainnet-geth-pbss-20250906-pruneancient.csv)
  - [mainnet-geth-pbss-20250806](dist/mainnet-geth-pbss-20250806.csv), [mainnet-geth-pbss-20250806-pruneancient](dist/mainnet-geth-pbss-20250806-pruneancient.csv)
  - [mainnet-geth-pbss-20250715](dist/mainnet-geth-pbss-20250715.csv), [mainnet-geth-pbss-20250715-pruneancient](dist/mainnet-geth-pbss-20250715-pruneancient.csv)
  - [mainnet-geth-pbss-20250605](dist/mainnet-geth-pbss-20250605.csv), [mainnet-geth-pbss-20250605-pruneancient](dist/mainnet-geth-pbss-20250605-pruneancient.csv)
  - [mainnet-geth-pbss-20250520](dist/mainnet-geth-pbss-20250520.csv), [mainnet-geth-pbss-20250520-pruneancient](dist/mainnet-geth-pbss-20250520-pruneancient.csv)
  - [mainnet-geth-pbss-20250501](dist/mainnet-geth-pbss-20250501.csv), [mainnet-geth-pbss-20250501-pruneancient](dist/mainnet-geth-pbss-20250501-pruneancient.csv)
  - [mainnet-geth-pbss-20250404](dist/mainnet-geth-pbss-20250404.csv), [mainnet-geth-pbss-20250404-pruneancient](dist/mainnet-geth-pbss-20250404-pruneancient.csv)
  - [mainnet-geth-pbss-20250310](dist/mainnet-geth-pbss-20250310.csv), [mainnet-geth-pbss-20250310-pruneancient](dist/mainnet-geth-pbss-20250310-pruneancient.csv)
- **testnet**:
  - [testnet-geth-pbss-20251013](dist/testnet-geth-pbss-20251013.csv), [testnet-geth-pbss-20251013-pruneancient](dist/testnet-geth-pbss-20251013-pruneancient.csv)
  - [testnet-geth-pbss-20250610](dist/testnet-geth-pbss-20250610.csv), [testnet-geth-pbss-20250610-pruneancient](dist/testnet-geth-pbss-20250610-pruneancient.csv)
  - [testnet-geth-pbss-20250407](dist/testnet-geth-pbss-20250407.csv), [testnet-geth-pbss-20250407-pruneancient](dist/testnet-geth-pbss-20250407-pruneancient.csv)
  - [testnet-geth-pbss-20240711.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240711.tar.lz4)(md5: 64626987189d739bd1a3ee743387f8a6)

## Source-2: Pruned FullNode(~900GB) & FastNode(~300GB) By 48Club
Usage: [https://github.com/BNB48Club/bsc-snapshots](https://github.com/BNB48Club/bsc-snapshots)
> Special thanks to [BNB48Club](https://x.com/48Club_Official) on contributing another dump of snapshot.

## Source-3: Erigon Mainnet Archive Node(~5TB)
Usage: [usage/erigon3_archivenode_usage.md](./usage/erigon3_archivenode_usage.md), Erigon 3 release: [v1.3.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.3.10)

> Endpoints: [erigon_51600000](dist/erigon_51600000.csv)

## Source-4: Reth BSC Snapshots

Usage: [reth-bsc snapshot usage](./usage/reth-bsc-snapshot.md)

### Snapshots (Monthly Update)
** Support for TrieDB will be discontinued. To use the v2 snapshots, do upgrade to Reth-bsc v0.0.10-beta or above. <br>
** v2 snapshots for archive MDBX will be available soon

| Type | Network | File | Size | Special Parameters |
| ---- | ------- | ---- | ---- | ------------------ |
| Archive MDBX | BSC-MainNet | [20260402_mainnet_reth_mdbx_static_files_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260302_mainnet_reth_mdbx_static_files_archive_node.tar.zst) <br> [20260402_mainnet_reth_mdbx_db_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260402_mainnet_reth_mdbx_db_archive_node.tar.zst) | 2.88 TiB <br> 3.45 TiB | `--db.max-size=12TB` <br> `--db.page-size=8KB` |
| Archive MDBX | BSC-TestNet | [20260710_testnet_reth_mdbx_archive_node_v2.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260710_testnet_reth_mdbx_archive_node_v2.tar.zst) | 404.90 GiB | - |
| Full MDBX | BSC-TestNet | [20260625_testnet_reth_mdbx_full_node_v2.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260625_testnet_reth_mdbx_full_node_v2.tar.zst) | 258.82 GiB | - |
| Full MDBX | BSC-MainNet | [20260626_mainnet_reth_mdbx_full_node_v2.tar.zst ](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260626_mainnet_reth_mdbx_full_node_v2.tar.zst) | 2.97 TiB | - |
| Full TrieDB | BSC-TestNet | [20260422_testnet_reth_triedb_full_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_testnet_reth_triedb_full_node.tar.zst) | 358.76 GiB | - |
| Full TrieDB | BSC-MainNet | [20260422_mainnet_reth_triedb_full_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_mainnet_reth_triedb_full_node.tar.zst) | 3.72 TiB | - |
| Archive TrieDB | BSC-TestNet | [20260422_testnet_reth_triedb_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_testnet_reth_triedb_archive_node.tar.zst) | 522.31 GiB | - |
| Archive TrieDB | BSC-MainNet | [20260422_mainnet_reth_triedb_static_files_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_mainnet_reth_triedb_static_files_archive_node.tar.zst) <br> [20260422_mainnet_reth_triedb_db_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_mainnet_reth_triedb_db_archive_node.tar.zst) <br> [20260422_mainnet_reth_triedb_triedb_archive_node.tar.zst](https://pub-c5400abe5bed4adbaf8cd47467747e74.r2.dev/20260422_mainnet_reth_triedb_triedb_archive_node.tar.zst) | 2.94 TiB <br> 3.54 TiB <br> 647.84 GiB | `--db.max-size=12TB` <br> `--db.page-size=8KB` |

## FAQ

### Why split snapshot into multiple files?

As the node snapshot of bsc becomes larger and larger, backup, upload and download will become increasingly unmaintainable, and it will occupy more disk space and take up more upload and download time.

At the same time, in order to support the history expiry and state expiry of bsc later, it is planned to split the node snapshot according to historical data and active data, and the following advantages can be obtained:

1. When updating the snapshot, only the changed part can be updated to reduce the difficulty of operation and maintenance;
2. Support annual backup of historical data, which also helps with the subsequent historical data pruning;
3. Support archiving multiple snapshot versions, avoiding wasting disk space;
4. Support downloading and decompressing a single part immediately, and snapshot download and decompression can be completed on a smaller disk;
