
### 3.1.Endpoints
> For more granular upload & download to avoid big files error, split the files into several chunks, so please download them together and concatenate finally.
#### a.Endpoint(Testnet): update every 6 months
> erigon version [v1.2.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.2.10), Block: [41637308](https://testnet.bscscan.com/block/41637308)
>
> md5 = 9bba1e9f5fa342879c070b93156dce76
>
> [testnet_erigon_DB_20240629.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/testnet_erigon_DB_20240629.tar.lz4)


#### b.Endpoint(Mainnet): update every three week
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


### 3.2.Usage

Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/node-real/bsc-erigon#system-requirements).
- BSC Archive: 8TB. BSC Full: 2TB.

Step 2: Download && Concatenate && Uncompress

```shell
sudo yum install aria2c
aria2c -s14 -x14 -k100M https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240416.lz4.[0]..erigon_data_20240416.lz4.[7]
lz4 -d erigon_data_20240416.lz4.[0]..erigon_data_20240416.lz4.[7]
cat "erigon_data_20240416"* > mdbx.dat

```
Step 3: Replace Data And Restart erigon
- Stop the running erigon client by `kill {pid}`
- Backing up the original data: `mv ${erigon_datadir}/chaindata/mdbx.dat  ${erigon_datadir}/chaindata/mdbx.dat `
- Replace the data: `mv ${erigon_snapshot_dir}/erigon/chaindata/mdbx.dat ${erigon_datadir}/chaindata/mdbx.dat`
- Replace the torrent: `mv ${erigon_torrent_dir}/snapshots ${erigon_datadir}/`
- Start the erigon client again and check logs

- mainnet command sample:
```shell
./build/bin/erigon --txpool.disable --metrics.addr=0.0.0.0 --log.console.verbosity=dbug --db.pagesize=16k --datadir ${erigon_dir/data} --private.api.addr=localhost:9090 --chain=bsc --metrics --log.dir.path ${erigon_dir/log}
```
- testnet command sample:
```shell
./build/bin/erigon --txpool.disable --networkid=97 --db.pagesize=16k --datadir ./data --chain=chapel --nat=any --log.dir.path ./log --http.port=8545 --private.api.addr=127.0.0.1:9090 --http --ws --http.api=web3,net,eth,debug,trace,txpool --http.addr=0.0.0.0 --torrent.download.rate=256mb --metrics --metrics.addr=0.0.0.0
```