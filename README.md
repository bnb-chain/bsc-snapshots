
# About BSC Snapshots
Currently, there are 3 sources of BSC snapshot could be used, if you are unclear about their differences, you may refer [Clarification of the snapshots](https://github.com/bnb-chain/bsc-snapshots/issues/349) first, to decide which snapshot suit you the most.

## Source-1: Legacy Full Node(~3TB)
Usage: [usage/legacyfullnode_usage.md](./usage/legacyfullnode_usage.md)

Endpoints:
> - **mainnet(monthly)**: [geth-pbss-pebble-20240802.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-pebble-20240802.tar.lz4)(md5: 05e689b53230cc2a5b064896aca09c53)
> - **testnet(every 6 months)**: [testnet-geth-pbss-20240711.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240711.tar.lz4)(md5: 64626987189d739bd1a3ee743387f8a6)

## Source-2: Pruned FullNode(~900GB) & FastNode(~300GB) By 48Club
Usage: [https://github.com/BNB48Club/bsc-snapshots](https://github.com/BNB48Club/bsc-snapshots)
> Special thanks to [BNB48Club](https://twitter.com/bnb48club) on contributing another dump of snapshot.

## Source-3: Erigon Archive Node(~8TB)
Usage: [usage/erigon_archivenode_usage.md](./usage/erigon_archivenode_usage.md)

Endpoints:
> - **Mainnet(monthly)**
> erigon version [v1.2.13](https://github.com/node-real/bsc-erigon/releases/tag/v1.2.13)
>
> SHA256(mdbx.dat) = 07baf99a5f7743bd83bf80f9f57cead12f3ad7d481bffc5c4a84bfbcd9f862f9
> 
> [erigon_data_20240803.lz4.000](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.000) md5=d4f9bb8086fdcb830526c695a17a3d12
> 
> [erigon_data_20240803.lz4.001](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.001) md5=c0c6512d47005d44174220ac912a1a69
> 
> [erigon_data_20240803.lz4.002](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.002) md5=af79d7a0a9b52588e479083f9fc3ed1a
>
> [erigon_data_20240803.lz4.003](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.003) md5=84dc5c02a03497f1b910cd08a8cabcb6
>
> [erigon_data_20240803.lz4.004](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.004) md5=067e9db5ff97fb6283c6598dc480e60d
>
> [erigon_data_20240803.lz4.005](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.005) md5=b4f514cf2fa6057c29fc88274c9d0c45
>
> [erigon_data_20240803.lz4.006](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.006) md5=7a8f03207b83b709c5d4b989ca8efa47
>
> [erigon_data_20240803.lz4.007](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240803.lz4.007) md5=ad7882164f8019f0fb1958df26d6a3fa
>
> [${erigon_datadir}/parlia/mdbx.dat](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/parlia/mdbx.dat) md5=073b5ce16ab6a30243ee50d426228db7
> 
> - **Testnet**
> No longer support erigon2 snapshot. Use the erigon3(No need extra snapshot) [v1.3.0-alpha1](https://github.com/node-real/bsc-erigon/releases/tag/v1.3.0-alpha1).

