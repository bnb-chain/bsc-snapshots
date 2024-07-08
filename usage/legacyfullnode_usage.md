# 1.About
The snapshot listed below are based the default mode(PBSS&Pebble). For other customized usage, pls refer [Advanced Usage](./usage/legacy_usage_advanced.md).
- mainnet: [geth-pbss-pebble-20240705.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-pebble-20240705.tar.lz4)(md5: 8efeec9f823015b114491a253727b8c8)
- testnet: [testnet-geth-pbss-20240607.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/testnet-geth-pbss-20240607.tar.lz4)(md5: 6ae3704330c71289cbed00204323451a)

# 2.Steps
## Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.bnbchain.org/bnb-smart-chain/developers/node_operators/node_best_practices/).
- A disk with enough free storage, at least twice the size of the snapshot.

## Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.lz4  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the background by `nohup wget -O geth.tar.gz  "<paste snapshot URL here>" &`


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


## Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs
