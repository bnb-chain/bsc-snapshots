
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
> erigon version [v1.2.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.2.10)
>
> SHA256(mdbx.dat) = 1d097e383fc5b0973d9eec18bdc1cc848352b2756a51fed48073c5d696383638
> 
> [erigon_data_20240625.lz4.000](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.000) md5=4461fe02ad1eb079ca6202f255acf4b3
> 
> [erigon_data_20240625.lz4.001](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.001) md5=6b6d6b7bb872df73cad0b56289303a75
> 
> [erigon_data_20240625.lz4.002](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.002) md5=a02dfec1edaaff671cd9ec4dd459074e
>
> [erigon_data_20240625.lz4.003](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.003) md5=a9f8e563f3aaeff5c2ce1bf4eedb3f1b
>
> [erigon_data_20240625.lz4.004](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.004) md5=61353dbe9b67c01ce77a0c3017d10a10
>
> [erigon_data_20240625.lz4.005](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.005) md5=98aad96c7a24efead991fe23c6af6ebb
>
> [erigon_data_20240625.lz4.006](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.006) md5=c3a96554962b5831ecd62a41829234bc
>
> [erigon_data_20240625.lz4.007](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.007) md5=f79cc9a1839aea4c11fe5e32e1f8931d
>
> [${erigon_datadir}/parlia/mdbx.dat](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/parlia/mdbx.dat) md5=073b5ce16ab6a30243ee50d426228db7
> 
> - **Testnet(every 6 months)**
>
> erigon version [v1.2.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.2.10), Block: [41637308](https://testnet.bscscan.com/block/41637308)
>
> [testnet_erigon_DB_20240629.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/testnet_erigon_DB_20240629.tar.lz4) md5 = 9bba1e9f5fa342879c070b93156dce76
> 
> [${erigon_datadir}/parlia/mdbx.dat](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/parlia/chapel/mdbx.dat) md5 = 44734d79bd3713c34f4dff0858d7ae9a

