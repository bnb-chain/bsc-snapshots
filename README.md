
# bsc-snapshots

## Database after Ancient Data Prune:

Ancient Data Prune is a new feature in [bsc v1.1.8](https://github.com/binance-chain/bsc/releases/tag/v1.1.8)

### Asia Endpoint


[geth-20220611.tar.lz4
](https://tf-dex-prod-public-snapshot-site1.s3-accelerate.amazonaws.com/geth-20220611-prune-ancient.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=dQYspfJiKdt92VRUbgBMJKjiLqY%3D&Expires=1657630639
)


## Pruned database:


### Asia Endpoint


[geth-20220611.tar.lz4
](https://tf-dex-prod-public-snapshot-site1.s3-accelerate.amazonaws.com/geth-20220611.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=aF84LEMAuOpY25fFqrgSDDlosek%3D&Expires=1657630638
)

### EU Endpoint


[geth-20220611.tar.lz4
](https://tf-dex-prod-public-snapshot.s3-accelerate.amazonaws.com/geth-20220611.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=OzQBJpyjofreE6jH2P0QI0uq20I%3D&Expires=1657630639
)


### US Endpoint


[geth-20220611.tar.lz4
](https://tf-dex-prod-public-snapshot-site3.s3-accelerate.amazonaws.com/geth-20220611.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=Ox%2BqrpgJxgGLWqtFFBymCbmb2UM%3D&Expires=1657630639
)

MD5 checksum: 227b16499199c8819ac86da804fe8d3b



# Usage 

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.binance.org/smart-chain/developer/fullnode.html).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.lz4  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.tar.gz  "<paste snapshot URL here?" &`


*If you need to speedup download, just use `aria2c`*
```
aria2c -o geth.tar.lz4 -x 4 -s 12 "URL TO ASIA ENDPOINT" "URL TO EU ENDPOINT" "URL TO US ENDPOINT"
```


- Uncompress: `tar -I lz4 -xvf geth.tar.lz4`. It will take more than two hours to uncompress. You can put it in the backgroud by `nohup tar -I lz4 xvf geth.tar.lz4 &`
- You can combine the above steps by running a script:
```
wget -O geth.tar.lz4  "<paste snapshot URL here>"
tar -I lz4 xvf geth.tar.lz4
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

