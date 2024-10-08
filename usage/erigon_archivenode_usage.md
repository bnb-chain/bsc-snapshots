# 1.Usage
## Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/node-real/bsc-erigon#system-requirements).
- BSC Archive: 10TB.

## Step 2: Download && Concatenate && Uncompress

```shell
sudo yum install aria2c
aria2c -s14 -x14 -k100M https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240625.lz4.[0]..erigon_data_20240625.lz4.[7]
lz4 -d erigon_data_20240625.lz4.[0]..erigon_data_20240625.lz4.[7]
cat "erigon_data_20240625"* > mdbx.dat
```

## Step 3: Replace Data And Restart erigon
- Stop the running erigon client by `kill {pid}`
- Backing up the original data: `mv ${erigon_datadir}/chaindata/mdbx.dat  ${erigon_datadir}/chaindata/mdbx.dat `
- Replace the data: `mv ${erigon_snapshot_dir}/erigon/chaindata/mdbx.dat ${erigon_datadir}/chaindata/mdbx.dat`
- Replace the parlia: `cd  ${erigon_datadir}/parlia/ && wget https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/parlia/mdbx.dat/`
- If you use the data/snapshots folder before, it need hours to run: `./integration stage_headers --reset --datadir=./data --chain=bsc`
- Start the erigon client again and check logs

- mainnet command sample:
```shell
./build/bin/erigon --txpool.disable --metrics.addr=0.0.0.0 --log.console.verbosity=dbug --db.pagesize=16k --datadir ${erigon_dir/data} --private.api.addr=localhost:9090 --chain=bsc --metrics --log.dir.path ${erigon_dir/log}
```
- testnet command sample:
```shell
./build/bin/erigon --txpool.disable --networkid=97 --db.pagesize=16k --datadir ./data --chain=chapel --nat=any --log.dir.path ./log --http.port=8545 --private.api.addr=127.0.0.1:9090 --http --ws --http.api=web3,net,eth,debug,trace,txpool --http.addr=0.0.0.0 --torrent.download.rate=256mb --metrics --metrics.addr=0.0.0.0
```

### FAQ

## Missing blocks 
```shell
    Because of the data has gap between chaindata/mdbx.dat and sanpshots/*.seg. It not affect node sync, but will affect the history data query. 
    use the latest release.
    make integration && ./integration stage_headers --reset --datadir=./data --chain=bsc
```

## No block headers to write
```shell
    Use the latest release
    Some time there are so many bad peers in the net. So  suggest remove the flag '--maxpeers' or set '--maxpeers = 10' to make sure the most peers are static node.
```

