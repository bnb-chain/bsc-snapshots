
# bsc-snapshots

Pruned database:

### Asia Endpoint


[geth-20211107.tar.gz
](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20211107.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=0D16ZJvV6iEOg92pCI%2FIRynWi8I%3D&Expires=1638883622
)

### EU Endpoint


[geth-20211107.tar.gz
](https://tf-dex-prod-public-snapshot.s3.amazonaws.com/geth-20211107.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=xLqGmda2xWCg%2BmMlNoADxKPn7KI%3D&Expires=1638883623
)


### US Endpoint


[geth-20211107.tar.gz
](https://tf-dex-prod-public-snapshot-site3.s3.amazonaws.com/geth-20211107.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=YkaV%2FrNOnQ4Y4Cl5hbZJ4c5CIrI%3D&Expires=1638883623
)

MD5 checksum: c1e741c764f306058591351491a11426



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

