
# bsc-snapshots

## 1.Legacy Full Node

The snapshot listed below are all PBSS&PebbleDB mode, if you need Hash based snapshot, check out [FAQ-Q2](https://github.com/bnb-chain/bsc-snapshots/issues/349)
### 1.1.Endpoints
**Path-Base-State-Scheme(recommand)**

- mainnet: [geth-pbss-pebble-20240612.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-pebble-20240612.tar.lz4)(md5: NA)
- testnet: [testnet-geth-pbss-20240607.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240607.tar.lz4)(md5: 6ae3704330c71289cbed00204323451a)

**Multi-Databases-PBSS(new feature)**
Multi-databases are a new feature in [bsc v1.4.6](https://github.com/bnb-chain/bsc/releases/tag/v1.4.6).
When the user runs node with the new snapshot of the multi-databases below, the feature will be enabled automatically.

- mainnet: [geth-pbss-multidatabase-20240428.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-multidatabase-20240428.tar.lz4)(md5: 644f1bb7dee97888825f92b748f79389)

### 1.2.Usage

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.bnbchain.org/bnb-smart-chain/developers/node_operators/node_best_practices/).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.lz4  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.tar.gz  "<paste snapshot URL here>" &`


*If you need to speedup download, just use `aria2c`*
```shell
aria2c -o geth.tar.lz4 -s14 -x14 -k100M https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/{filename}
```

But aria2c may fail sometimes, you need to rerun the download command. To make it convient, you can use the following script, save it into file `download.sh` and run: `nohup ./download.sh "<paste snapshot URL here>" <your dir> &`
```bash
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
```shell
wget -O geth.tar.lz4  "<paste snapshot URL here>"
tar -I lz4 -xvf geth.tar.lz4
```


- If you do not need to store the archive for use with other nodes, you may also extract it while downloading to save time and disk space:
```shell
wget -q -O - <snapshot URL> | tar -I lz4 -xvf -
```


Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs

### 1.3.About Snapshot with multi-database

The Chaindata of the snapshot will be divided into three stores, BlockStore, TrieStore, and OriginalStore.

TrieStore: All trie nodes of the current state and historical state data of nearly 9w blocks are stored here. The data is stored in  ${BSC_DataDir}/geth/chaindata/state.

BlockStore: Block-related data is stored in this store, including headers, bodies, receipts, difficulties, number-to-hash indexes, hash-to-number indexes,
and historical block data. The data is stored in ${BSC_DataDir}/geth/chaindata/block.

If the user intends to store the databases on the same storage disk, they just need to start the client by following the same steps after extracting the snap file, without requiring any additional startup parameters.

If the user want to store different databases on different disks, you can move the folder corresponding to TrieStore or BlockStore to a different directory and create a symbolic link with the same name as the folder using an absolute path in the chaindata directory.
For example:
```
mv ${BSC_DataDir}/geth//chaindata/state <move-directory>
ln -s <move-directory>  ${BSC_DataDir}/geth/chaindata/state
```
After the symbolic link is created, you can start the bsc client again and check the logs.
Due to the larger size of the trie store, we recommend that the trie database be stored on different disks to achieve better performance.

## 2.Snapshots Provided by Community

Special thanks to [BNB48Club](https://twitter.com/bnb48club) on contributing another dump of snapshot, you can also refer [here](https://github.com/BNB48Club/bsc-snapshots) to download.

## 3.Erigon-BSC Snapshot(Archive Node)

### 3.1.Endpoints
> For more granular upload & download to avoid big files error, split the files into several chunks, so please download them together and concatenate finally.
#### a.Endpoint(Testnet): update every 6 months
> erigon version [v1.1.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.1.10), Block: [35851654](https://testnet.bscscan.com/block/35851654)
>
> SHA256 = 7c59f6846eba146a5668e44d3863545375ee52c6c70d3707ab55c2d8fdfdc6bb
>
> [testnet_erigon_DB_20231211.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/testnet_erigon_DB_20231211.tar.lz4)


#### b.Endpoint(Mainnet): update every three week
> erigon version [v1.2.8](https://github.com/node-real/bsc-erigon/releases/tag/v1.2.8)
>
> SHA256(mdbx.dat) = 31fdebebe89ab25bf5842fa2055428a14281c8279ce2499eef93fece5a94deea
> 
> [erigon_data_20240520.lz4.000](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.000) md5=5983392858e54bf40e05853294399303
> 
> [erigon_data_20240520.lz4.001](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.001) md5=14ac48c4f866c6f754ac3a2c661d6eb4
> 
> [erigon_data_20240520.lz4.002](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.002) md5=c7c95f96200d35b81e52d50f8ed52ebf
>
> [erigon_data_20240520.lz4.003](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.003) md5=2f2d918363c992bb9254dd6504d8a541
>
> [erigon_data_20240520.lz4.004](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.004) md5=9cd5075e8e611a35c44eec3cd31305f0
>
> [erigon_data_20240520.lz4.005](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.005) md5=0bd256afaf42bfb4b163354142cfda0d
>
> [erigon_data_20240520.lz4.006](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.006) md5=4f31de846555841326fa04ccd00b5b67
>
> [erigon_data_20240520.lz4.007](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240520.lz4.007) md5=e2750053a2656b6cbaf743459480c144

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
./build/bin/erigon --p2p.protocol=66 --txpool.disable --metrics.addr=0.0.0.0 --log.console.verbosity=dbug --db.pagesize=16k --datadir ${erigon_dir/data} --private.api.addr=localhost:9090 --chain=bsc --metrics --log.dir.path ${erigon_dir/log}
```
- testnet command sample:
```shell
./build/bin/erigon --txpool.disable --networkid=97 --db.pagesize=16k --p2p.protocol=66 --datadir ./data --chain=chapel --sentry.drop-useless-peers --nat=any --log.dir.path ./log --http.port=8545 --private.api.addr=127.0.0.1:9090 --http --ws --http.api=web3,net,eth,debug,trace,txpool --http.addr=0.0.0.0 --torrent.download.rate=256mb --metrics --metrics.addr=0.0.0.0
```
