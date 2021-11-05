
# bsc-snapshots

Pruned database:

### Asia Endpoint

verified:

[new-geth-20211104.tar.gz](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/new-geth-20211104.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=5Ll3tOk9dSuvieVekXUVHeGLuAE%3D&Expires=1638670592)

### EU Endpoint


verified:

[new-geth-20211104.tar.gz](https://tf-dex-prod-public-snapshot.s3.amazonaws.com/new-geth-20211104.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=9KSe9AzSQbXcOtzAETQ%2B4igfX5I%3D&Expires=1638711052)

### US Endpoint

verified:

[new-geth-20211104.tar.gz](https://tf-dex-prod-public-snapshot-site3.s3.amazonaws.com/new-geth-20211104.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=84llt3NKCrz82iaa8KdFtWP2Diw%3D&Expires=1638710999)



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

Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs

