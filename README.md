
# bsc-snapshots


## Database after Ancient Data Prune:

Ancient Data Prune is a new feature in [bsc v1.1.8](https://github.com/bnb-chain/bsc/releases/tag/v1.1.8)


### Endpoint

Here are snapshots of HBSS with leveldb and PBSS snapshots with pebble.

**Path-Base-State-Scheme(recommand)**

- mainnet: [geth-pbss-pebble-20240320.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-pebble-20240320.tar.lz4)

  md5: c23287b769ca4beba28324300555cf01
- testnet: [testnet-geth-pbss-20240307.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240307.tar.lz4)

  md5: da9cac9b702123f63f9254c1de698eab

**Hash-Base-State-Scheme(not recommand)**
> Warning: will stop maintain hash base snapshot after Mid Mar 2024

- mainnet:[geth-20240320.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-20240320.tar.lz4)

  md5: d7bb69f44897467ada3b81037fdf0ccb
- testnet: [testnet-geth-20240321.tar.lz4](https://pub-5809538c476542388ad6ca3e681ea85f.r2.dev/testnet-geth-20240321.tar.lz4)
 
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


## Erigon-BSC Snapshot(Archive Node)

> For more granular upload & download to avoid big files error, split the files into several chunks, so please download them together and concatenate finally.
### Endpoint(Testnet): update every 6 months
> erigon version [v1.1.10](https://github.com/node-real/bsc-erigon/releases/tag/v1.1.10), Block: [35851654](https://testnet.bscscan.com/block/35851654)
#### [testnet_erigon_DB_20231211.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/testnet_erigon_DB_20231211.tar.lz4)
#### SHA256 = 7c59f6846eba146a5668e44d3863545375ee52c6c70d3707ab55c2d8fdfdc6bb

### Endpoint(Mainnet): update every three week
> erigon version [v1.1.14](https://github.com/node-real/bsc-erigon/releases/tag/v1.1.13)
#### [erigon_data_20240302.lz4.000](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.000) md5=dfcec1a1f46fcb5d9396a92c351faf40
#### [erigon_data_20240302.lz4.001](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.001) md5=cc6b1bb1e2189d9e262698f7f5804f42
#### [erigon_data_20240302.lz4.002](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.002) md5=a5256719150b20f4eda7824ddc7f16d2
#### [erigon_data_20240302.lz4.003](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.003) md5=dd055f7c412ca859cadd5e2c6e8cc1a9
#### [erigon_data_20240302.lz4.004](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.004) md5=864cafd4c7688be051a464ac7a25751a
#### [erigon_data_20240302.lz4.005](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.005) md5=026a412fe732c38689ddf65b8e5ef36f
#### [erigon_data_20240302.lz4.006](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.006) md5=04064472fb1f8949b1e41aed31004509
#### [erigon_data_20240302.lz4.007](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.007) md5=313ac4c2f87c77fa54991462caa63c09

### Endpoint(Mainnet torrent,the block range[0, 36,500,000))
#### [erigon_snapshots_20240301.tar.lz4](https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_snapshots_20240301.tar.lz4/erigon_snapshots_20240301.tar.lz4) md5=04238a8fb079904f4f1c8a9862054d7e

### Usage

Step 1: Preparation

- Make sure your hardware meets the [suggested requirement](https://github.com/node-real/bsc-erigon#system-requirements).
- BSC Archive: 8TB. BSC Full: 2TB.

Step 2: Download && Concatenate && Uncompress

```shell
sudo yum install aria2c
aria2c -s14 -x14 -k100M https://pub-60a193f9bd504900a520f4f260497d1c.r2.dev/erigon_data_20240302.lz4.[0]..erigon_data_20240302.lz4.[7]
cat "erigon_data_20240302.lz4."* > combined_compressed_file.lz4
lz4 -d combined_compressed_file.lz4 mdbx.dat
# or
cat "erigon_data_20240302.lz4."* | lz4 -d -c > mdbx.dat
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
