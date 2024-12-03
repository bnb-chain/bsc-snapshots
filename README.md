
# About BSC Snapshots
Currently, there are 3 sources of BSC snapshot could be used, if you are unclear about their differences, you may refer [Clarification of the snapshots](https://github.com/bnb-chain/bsc-snapshots/issues/349) first, to decide which snapshot suit you the most.

## Source-1: Legacy Full Node(~3TB)
Usage: [usage/legacyfullnode_usage.md](./usage/legacyfullnode_usage.md)

### mainnet(monthly update)

Latest Snapshot: mainnet-geth-pbss-20241202.

| file                                                                                                                                       | md5                              | size     |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | -------- |
| [mainnet-geth-pbss-blocks-10512000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-blocks-10512000.tar.lz4) | 3a973854371e526be8dbbce63aad855b | 289.91GB |
| [mainnet-geth-pbss-blocks-21024000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-blocks-21024000.tar.lz4) | ef20506070cbe2deb3b0c3c5cae3149d | 601.39GB |
| [mainnet-geth-pbss-blocks-31536000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-blocks-31536000.tar.lz4) | 7ed223135e0bb50fdcf625529d89b83c | 376.89GB |       
| [mainnet-geth-pbss-blocks-42048000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-blocks-42048000.tar.lz4) | 6a21f55892f6da5f6ca5b77f6c0d88bd | 532.23GB |
| [mainnet-geth-pbss-blocks-44431618.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-blocks-44431618.tar.lz4) | 87fe61c41ae62170c915e0f2ff649f62 | 106.09GB |     
| [mainnet-geth-pbss-base-44521618.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/mainnet-geth-pbss-base-44521618.tar.lz4)     | 8afc09a4d44ba6041e2b666f97218700 | 869.10GB | 

### testnet(update every 4 months)

Latest Snapshot: testnet-geth-pbss-20241203.

| file                                                                                                                                       | md5                              | size     |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | -------- |
| [testnet-geth-pbss-blocks-10512000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-blocks-10512000.tar.lz4) | 5c4efc11b698d26f1c085b9b4796222d | 11.77GB  |
| [testnet-geth-pbss-blocks-21024000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-blocks-21024000.tar.lz4) | 7378acc5b51c52f34e4e02497c719804 | 35.94GB  |
| [testnet-geth-pbss-blocks-31536000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-blocks-31536000.tar.lz4) | 0428e85d9771a5664e0053305ec30e23 | 35.46GB  |
| [testnet-geth-pbss-blocks-42048000.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-blocks-42048000.tar.lz4) | 60e1af49b60e23d795e5375b88b8a613 | 72.20GB  |
| [testnet-geth-pbss-blocks-46068492.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-blocks-46068492.tar.lz4) | b7e4e24722a3ec91ade323673cfbe303 | 11.84GB  |
| [testnet-geth-pbss-base-46158492.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-base-46158492.tar.lz4)     | 993e19a531f570bd0756fc6b8194e9ab | 111.27GB |

### download

You can download the mainnet or testnet files separately in the list and unzip them in a same directory. Or you can use the following script:

```bash
wget https://raw.githubusercontent.com/bnb-chain/bsc-snapshots/main/dist/fetch-snapshot.sh

# download & checksum the mainnet or testnet snapshot
bash fetch-snapshot.sh -d -c -D {download_dir} {mainnet-geth-pbss-20241202|testnet-geth-pbss-20241203}

# extract the downloaded snapshot
bash fetch-snapshot.sh -e -D {download_dir} -E {extract_dir} {mainnet-geth-pbss-20241202|testnet-geth-pbss-20241203}
```

You can remove the `-c` option to skip md5 checking. You can use help to get more detailed command parameters.

```bash
bash fetch-snapshot.sh --help
# download, checksum, extract the snapshot, it need at least 6TB empty size for mainnet.
bash fetch-snapshot.sh -d -e -c -D {download_dir} -E {extract_dir} {snapshot_name}
# download, checksum, extract the snapshot, and auto delete the decompressed file, it need at least 4TB empty size for mainnet.
bash fetch-snapshot.sh -d -e -c --auto-delete -D {download_dir} -E {extract_dir} {snapshot_name}
```

### Previous snapshot

> - **mainnet(monthly)**: [geth-pbss-pebble-20241028.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-pebble-20241028.tar.lz4)(md5: 50d63167e825a4e53258c4655d8ce040)
> - **testnet(every 6 months)**: [testnet-geth-pbss-20240711.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240711.tar.lz4)(md5: 64626987189d739bd1a3ee743387f8a6)

## Source-2: Pruned FullNode(~900GB) & FastNode(~300GB) By 48Club
Usage: [https://github.com/BNB48Club/bsc-snapshots](https://github.com/BNB48Club/bsc-snapshots)
> Special thanks to [BNB48Club](https://x.com/48Club_Official) on contributing another dump of snapshot.

## Source-3: Erigon Archive Node(~5TB)
Usage: [usage/erigon3_archivenode_usage.md](./usage/erigon3_archivenode_usage.md), Erigon 3 release: [v1.3.0-alpha4](https://github.com/node-real/bsc-erigon/releases/tag/v1.3.0-alpha4)

> Endpoints: Since Erigon 3, snapshot is no longer needed.

## FAQ

### Why split snapshot into multiple files?

As the node snapshot of bsc becomes larger and larger, backup, upload and download will become increasingly unmaintainable, and it will occupy more disk space and take up more upload and download time.

At the same time, in order to support the history expiry and state expiry of bsc later, it is planned to split the node snapshot according to historical data and active data, and the following advantages can be obtained:

1. When updating the snapshot, only the changed part can be updated to reduce the difficulty of operation and maintenance;
2. Support annual backup of historical data, which also helps with the subsequent historical data pruning;
3. Support archiving multiple snapshot versions, avoiding wasting disk space;
4. Support downloading and decompressing a single part immediately, and snapshot download and decompression can be completed on a smaller disk;