
# bsc-snapshots


## Database after Ancient Data Prune:

Ancient Data Prune is a new feature in [bsc v1.1.8](https://github.com/bnb-chain/bsc/releases/tag/v1.1.8)


### Endpoint


[geth-20230719.tar.lz4
](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-20230719.tar.lz4
)




## Snapshots Provided by Community

Special thanks to [BNB48Club](https://twitter.com/bnb48club) on contributing another dump of snapshot, you can also refer [here](https://github.com/BNB48Club/bsc-snapshots) to download.



### Usage 

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.bnbchain.org/docs/validator/fullnode).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.lz4  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.tar.gz  "<paste snapshot URL here>" &`


*If you need to speedup download, just use `aria2c`*
```
aria2c -o geth.tar.lz4 -s14 -x14 -k100M https://download.bsc-snapshot.workers.dev/{filename}
```

But aria2c may fail sometimes, you need to rerun the download command. To make it convient, you can use the follow script
```
#!/bin/bash
if [ $# -eq 1 ]; then 
        dir=$(pwd)
elif [ $# -eq 2 ]; then 
        dir=$2
else 
        echo "Usage: $0 <uri> [filepath] "
        exit 1
fi
uri=$1
filename=$(basename "$uri")
status=-1
while (( status != 0 ))
do 
        PIDS=$(pgrep aria2c)
        if [ -z "$PIDS" ]; then
                aria2c -d $dir -o $filename -s14 -x14 -k100M $uri
        fi
        status=$?
        pid=$(pidof aria2c)
        wait $pid 
        echo aria2c exit.
        case $status in 
                3)
                        echo file not exist.
                        exit 3
                        ;;
                9)
                        echo No space left on device.
                        exit 9
                        ;;
                *)
                        continue
                        ;;
        esac
done
echo download succeed.
exit 0
```


- Uncompress: `tar -I lz4 -xvf geth.tar.lz4`. It will take more than two hours to uncompress. You can put it in the background by `nohup tar -I lz4 -xvf geth.tar.lz4 &`
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


## Erigon-BSC Snapshot(Archive Node)

> For more granular upload & download to avoid big files error, split the files into several chunks, so please download them together and concatenate finally.
### Endpoint(Testnet): will update quarterly
> erigon version [v1.1.4](https://github.com/node-real/bsc-erigon/releases/tag/v1.1.4), Block: [31205834](https://testnet.bscscan.com/block/31205834)
#### [testnet_erigon_DB_20230702.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/testnet_erigon_DB_20230702.tar.lz4/testnet_erigon_DB_20230702.tar.lz4)

### Endpoint(Mainnet): update bi-weekly
> erigon version [v1.1.4](https://github.com/node-real/bsc-erigon/releases/tag/v1.1.4)
#### [erigon_data_20230724_chunkaa](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724aa)
#### [erigon_data_20230724_chunkab](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724ab)
#### [erigon_data_20230724_chunkac](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724ac)
#### [erigon_data_20230724_chunkad](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724ad)
#### [erigon_data_20230724_chunkae](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724ae)
#### [erigon_data_20230724_chunkaf](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_202307240af)
#### [erigon_data_20230724_chunkag](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunk_20230724ag)

### Usage

Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/node-real/bsc-erigon#system-requirements).
- BSC Archive: 8TB. BSC Full: 2TB.

Step 2: Download && Concatenate && Uncompress

```
sudo yum install aria2c
aria2c -s14 -x14 -k100M https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/chunka[a]..chunka[g]
cat ./chunk* > mdbx.tar.lz4
tar -I lz4 -xvf mdbx.tar.lz4
```
Step 3: Replace Data And Restart erigon
- Stop the running erigon client by `kill {pid}`
- Backing up the original data: `mv ${erigon_datadir}/chaindata/mdbx.dat  ${erigon_datadir}/chaindata/mdbx.dat `
- Replace the data: `mv ${erigon_snapshot_dir}/erigon/chaindata/mdbx.dat ${erigon_datadir}/chaindata/mdbx.dat`
- Start the erigon client again and check logs

- mainnet command sample: 
```shell
./build/bin/erigon --sentry.drop-useless-peers --p2p.protocol=66 --txpool.disable --metrics.addr=0.0.0.0 --log.console.verbosity=dbug --db.pagesize=16k --datadir ${erigon_dir/data} --private.api.addr=localhost:9090 --chain=bsc --metrics --log.dir.path ${erigon_dir/log}
```
-testnet command sample
```shell
./build/bin/erigon --txpool.disable --networkid=97 --db.pagesize=16k --p2p.protocol=66 --datadir ./data --chain=chapel --sentry.drop-useless-peers --nat=any --log.dir.path ./log --http.port=8545 --private.api.addr=127.0.0.1:9090 --http --ws --http.api=web3,net,eth,debug,trace,txpool --http.addr=0.0.0.0 --torrent.download.rate=256mb --metrics --metrics.addr=0.0.0.0
```


