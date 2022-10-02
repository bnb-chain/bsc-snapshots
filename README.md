
# bsc-snapshots


## Database after Ancient Data Prune:

Ancient Data Prune is a new feature in [bsc v1.1.8](https://github.com/binance-chain/bsc/releases/tag/v1.1.8)


### Endpoint


[geth-20221002.tar.lz4
](https://download.bsc-snapshot.workers.dev/geth-20221002.tar.lz4
)

MD5 checksum: 216cb9d92db14f2563738b80c255febf



## Snapshots Provided by Community

Special thanks to [BNB48Club](https://twitter.com/bnb48club) on contributing another dump of snapshot, you can also refer [here](https://github.com/BNB48Club/bsc-snapshots) to download.



### Usage 

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.binance.org/smart-chain/developer/fullnode.html).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.lz4  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.tar.gz  "<paste snapshot URL here?" &`


*If you need to speedup download, just use `aria2c`*
```
aria2c -o geth.tar.lz4 -s14 -x14 -k100M https://download.bsc-snapshot.workers.dev/{filename} -o geth.tar.lz4
```


- Uncompress: `tar -I lz4 -xvf geth.tar.lz4`. It will take more than two hours to uncompress. You can put it in the backgroud by `nohup tar -I lz4 -xvf geth.tar.lz4 &`
- You can combine the above steps by running a script:
```
wget -O geth.tar.lz4  "<paste snapshot URL here>"
tar -I lz4 -xvf geth.tar.lz4
```


- If you do not need to store the archive for use with other nodes, you may also extract it while downloading to save time and disk space:
```
wget -q -O - <snapshot URL> | tar -I lz4 -xvf -
```


Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs

## Erigon Snapshot

> erigon version [v2022.07.04](https://github.com/ledgerwatch/erigon/releases/tag/v2022.07.04)
### Endpoint
[erigon-20220806.tar.lz4](https://download.bsc-snapshot.workers.dev/snapshot/erigon-20220806.tar.lz4
)


### Usage

Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/ledgerwatch/erigon#system-requirements).
- A fullnode running BSC requires at least 2TB of space

Step 2: Download && Uncompress

```
sudo yum install aria2c
aria2c -s14 -x14 -k100M https://download.bsc-snapshot.workers.dev/{filename} -o erigon.tar.lz4
tar -I lz4 -xvf geth.tar.lz4
```
Step 3: Replace Data And Restart erigon
- Stop the running erigon client by `kill {pid}`
- Backing up the original data: `mv ${erigon_datadir}/erigon ${erigon_datadir}/erigon_back`
- Replace the data: `mv ${erigon_snapshot_dir}/erigon ${erigon_datadir}`
- Start the erigon client again and check logs

```shell
./erigon --chain=bsc --prune= --prune.h.older=5000 --prune.r.older=5000 --prune.t.older=5000 --prune.c.older=5000 --db.pagesize=16k --datadir ${erigon_datadir}/erigon --private.api.addr=localhost:9090 -metrics --metrics.addr=0.0.0.0 --metrics.port=9350 --pprof --pprof.addr=0.0.0.0 --pprof.port=9351
```


