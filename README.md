
# About BSC Snapshots
Currently, there are 3 sources of BSC snapshot could be used, if you are unclear about their differences, you may refer [Clarification of the snapshots](https://github.com/bnb-chain/bsc-snapshots/issues/349) first, to decide which snapshot suit you the most.

## Source-1: Legacy Full Node
Usage: [usage/legacyfullnode_usage.md](./usage/legacyfullnode_usage.md)

> Currently, snapshots are provided as block history data divided by year. Each list includes world states, historical block files, URL, MD5, file size. Users can use the provided tools to quickly download.

> The Pruned Snapshot is better for internal/private nodes, it only keeps the latest 9w historical blocks and requires BSC client >=[v1.5.5](https://github.com/bnb-chain/bsc/releases/tag/v1.5.5).

### mainnet(monthly update)

| Snapshot Type   | Snapshot File                                                                               | Total Size | Remark        |
|-----------------|---------------------------------------------------------------------------------------------|------------|---------------|
| Full Snapshot   | [mainnet-geth-pbss-20250605](dist/mainnet-geth-pbss-20250605.csv)                           | **~3TB**   |               |
| Pruned Snapshot | [mainnet-geth-pbss-20250605-pruneancient](dist/mainnet-geth-pbss-20250605-pruneancient.csv) | **~900GB** | BSC >= v1.5.5 |

### testnet(update every 4 months)

| Snapshot Type   | Snapshot File                                                                               | Total Size | Remark        |
|-----------------|---------------------------------------------------------------------------------------------|------------|---------------|
| Full Snapshot   | [testnet-geth-pbss-20250407](dist/testnet-geth-pbss-20250407.csv)                           | **~300GB** |               |
| Pruned Snapshot | [testnet-geth-pbss-20250407-pruneancient](dist/testnet-geth-pbss-20250407-pruneancient.csv) | **~120GB** | BSC >= v1.5.5 |

### Download

You can download the mainnet or testnet files separately in the list and unzip them in a same directory. Or you can use the following script:

```bash
# install aria2 on your os
yum install aria2
wget https://raw.githubusercontent.com/bnb-chain/bsc-snapshots/main/dist/fetch-snapshot.sh

# download & checksum the mainnet or testnet snapshot
bash fetch-snapshot.sh -d -c -D {download_dir} {mainnet-geth-pbss-20250404|testnet-geth-pbss-20250407}
# download & checksum the pruned mainnet or testnet snapshot
bash fetch-snapshot.sh -d -c -p -D {download_dir} {mainnet-geth-pbss-20250208}

# extract the downloaded snapshot
bash fetch-snapshot.sh -e -D {download_dir} -E {extract_dir} {mainnet-geth-pbss-20250404|testnet-geth-pbss-20250407}
```

You can remove the `-c` option to skip md5 checking. You can use help to get more detailed command parameters.

```bash
bash fetch-snapshot.sh --help
# download, checksum, extract the snapshot, it need at least 6TB empty size for mainnet.
bash fetch-snapshot.sh -d -e -c -D {download_dir} -E {extract_dir} {snapshot_name}
# download, checksum, extract the snapshot, and auto delete the decompressed file, it need at least 4TB empty size for mainnet.
bash fetch-snapshot.sh -d -e -c --auto-delete -D {download_dir} -E {extract_dir} {snapshot_name}
# download, checksum, extract the pruned snapshot, and auto delete the decompressed file, it need at least 2TB empty size for mainnet.
bash fetch-snapshot.sh -d -e -c -p --auto-delete -D {download_dir} -E {extract_dir} {snapshot_name}
```

> Please keep `fetch-snapshot.sh` the latest version.

### Previous snapshot

- **mainnet**:
  - [mainnet-geth-pbss-20250520](dist/mainnet-geth-pbss-20250520.csv), [mainnet-geth-pbss-20250520-pruneancient](dist/mainnet-geth-pbss-20250520-pruneancient.csv)
  - [mainnet-geth-pbss-20250501](dist/mainnet-geth-pbss-20250501.csv), [mainnet-geth-pbss-20250501-pruneancient](dist/mainnet-geth-pbss-20250501-pruneancient.csv)
  - [mainnet-geth-pbss-20250404](dist/mainnet-geth-pbss-20250404.csv), [mainnet-geth-pbss-20250404-pruneancient](dist/mainnet-geth-pbss-20250404-pruneancient.csv)
  - [mainnet-geth-pbss-20250310](dist/mainnet-geth-pbss-20250310.csv), [mainnet-geth-pbss-20250310-pruneancient](dist/mainnet-geth-pbss-20250310-pruneancient.csv)
- **testnet**:
  - [testnet-geth-pbss-20240711.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240711.tar.lz4)(md5: 64626987189d739bd1a3ee743387f8a6)

## Source-2: Pruned FullNode(~900GB) & FastNode(~300GB) By 48Club
Usage: [https://github.com/BNB48Club/bsc-snapshots](https://github.com/BNB48Club/bsc-snapshots)
> Special thanks to [BNB48Club](https://x.com/48Club_Official) on contributing another dump of snapshot.

## Source-3: Erigon Mainnet Archive Node(~5TB)
Usage: [usage/erigon3_archivenode_usage.md](./usage/erigon3_archivenode_usage.md), Erigon 3 release: [v1.3.0-alpha4](https://github.com/node-real/bsc-erigon/releases/tag/v1.3.0-alpha4)

> Endpoints: [erigon_48000000](dist/erigon-48000000.csv)

## FAQ

### Why split snapshot into multiple files?

As the node snapshot of bsc becomes larger and larger, backup, upload and download will become increasingly unmaintainable, and it will occupy more disk space and take up more upload and download time.

At the same time, in order to support the history expiry and state expiry of bsc later, it is planned to split the node snapshot according to historical data and active data, and the following advantages can be obtained:

1. When updating the snapshot, only the changed part can be updated to reduce the difficulty of operation and maintenance;
2. Support annual backup of historical data, which also helps with the subsequent historical data pruning;
3. Support archiving multiple snapshot versions, avoiding wasting disk space;
4. Support downloading and decompressing a single part immediately, and snapshot download and decompression can be completed on a smaller disk;
