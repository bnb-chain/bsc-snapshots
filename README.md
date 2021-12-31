
# bsc-snapshots

Pruned database:

### Asia Endpoint


[geth-20211231.tar.lz4
](https://tf-dex-prod-public-snapshot-site1.s3-accelerate.amazonaws.com/geth-20211231.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=rdgsxvIpNua8BTvITZuLeTFsd8E%3D&Expires=1643581056
)

### EU Endpoint


[geth-20211231.tar.lz4
](https://tf-dex-prod-public-snapshot.s3-accelerate.amazonaws.com/geth-20211231.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=yUwoFhNGZdr%2Fs%2BWp6x3gCBPq42M%3D&Expires=1643581056
)


### US Endpoint


[geth-20211231.tar.lz4
](https://tf-dex-prod-public-snapshot-site3.s3-accelerate.amazonaws.com/geth-20211231.tar.lz4?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=uobA1GKKp1kKbCdpIOnqssRwjNg%3D&Expires=1643581057
)

MD5 checksum: f42774f1ee9521a3f9bf68fa19e78426



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

