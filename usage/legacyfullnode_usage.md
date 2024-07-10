# 1.Usage
## Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.bnbchain.org/bnb-smart-chain/developers/node_operators/node_best_practices/).
- A disk with enough free storage, at least twice the size of the snapshot.

## Step 2: Download
*As the snapshot is getting larger, now it is difficult to download it by simply `wget`, you need to use `aria2c` as it supports resumable transmission. And `aria2c` may fail sometimes, we provide a script to make it easier.*
- Copy the above snapshot URL.
- install it first: `sudo yum install aria2c`
- download the script: [download.sh](./download.sh)
- run: `nohup ./download.sh "<paste snapshot URL here>" <your dir> &`

## Step 3: Uncompress
- Uncompress will take more than two hours, put it in the background by `nohup tar -I lz4 -xvf geth.tar.lz4 &`


## Step 4: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data if needed: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata`
- Start the bsc client again and check the logs

# 2.Advanced Usage
The snapshot listed homepage are based the default mode(PBSS&Pebble). For other customized usage, pls refer [Advanced Usage](./legacyfullnode_usage_advanced.md).

