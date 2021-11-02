
# bsc-snapshots

Pruned database:

### Asia endpoint:

[geth-20211031.tar.gz
](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20211031.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=ESK5xmr5f1AIK4Mr6our%2FALXzQk%3D&Expires=1638310885
)


### EU  endpoint:

[geth-20211101.tar.gz
](https://tf-dex-prod-public-snapshot.s3.amazonaws.com/geth-20211101.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=r7DrUr9zv5vpACS4pGSXLwOR78A%3D&Expires=1638455710
)




# Usage 

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.binance.org/smart-chain/developer/fullnode.html).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.tar.gz  "<paste snapshot URL here>"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.tar.gz  "<paste snapshot URL here?" &`
- Uncompress: `tar zxvf geth.tar.gz` or `tar -I pigz -xvf geth.tar.gz`. It will take more than two hours to uncompress. You can put it in the backgroud by `nohup tar zxvf geth.tar.gz &`
- You can combine the above steps by running a script:
```
wget -O geth.tar.gz  "<paste snapshot URL here>"
tar zxvf geth.tar.gz
```
- If you do not need to store the archive for use with other nodes, you may also extract it while downloading to save time and disk space:
```
wget -q -O - <snapshot URL> | tar -zxvf -
```

Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs

