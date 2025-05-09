# 1.Usage

Erigon 3 has been supported on the BNB Smart Chain (BSC) since early August 2024, significantly reducing the disk space requirements for operating a BSC archive node and simplifying the process. For further details, please refer to the article [Erigon 3 - New version of BSC Erigon Client](https://www.bnbchain.org/en/blog/erigon-3-new-version-of-bsc-erigon-client-reduced-sync-time-from-weeks-to-10-hours-2).

## Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/node-real/bsc-erigon#system-requirements).
- BSC Mainnet Archive: 5TB
- BSC Testnet Archive: 500GB

## Step 2: Sync With Erigon 3

It is extremely easy to run a BSC archive node with Erigon 3, you don't need to download any data, just make sure your device meets the hardware requirement, download [the latest BSC Erigon 3 Release](https://github.com/node-real/bsc-erigon/releases/tag/v1.3.0-alpha4) and run the following command.

- mainnet command sample:
```shell
./erigon --chain=bsc --datadir=${erigon_dir/data} --db.size.limit=1T --batchSize=2g --private.api.addr=localhost:9090 --http.port=8545 --port 30303  --http --ws --http.api=web3,net,eth,trace,txpool --log.console.verbosity=3 --log.dir.path ${erigon_dir/log} --authrpc.port=8551 --diagnostics.disabled
```
- testnet command sample:
```shell
./erigon --chain=chapel --datadir=${erigon_dir/data} --db.size.limit=1T --batchSize=2g --private.api.addr=localhost:9090 --http.port=8545 --port 30303  --http --ws --http.api=web3,net,eth,trace,txpool --log.console.verbosity=3 --log.dir.path ${erigon_dir/log} --authrpc.port=8551 --diagnostics.disabled
```

# 2.FAQ
NA
