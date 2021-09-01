# bsc-snapshots

Pruned database:

[Bsc-20210830.zip](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20210830.zip?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Expires=1632969271&Signature=I8RvQgUXakavyMFhWLxxrsPFrn8%3D) (size 461.0GB)

MD5 checksum: 511f2f6cfae216f12000521b4122f771

# Usage 

Step 1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.binance.org/smart-chain/developer/fullnode.html).
- A disk with enough free storage, at least twice the size of the snapshot.

Step 2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.zip  "{paste snapshot URL here}"` . It will take one or two hours to download the snapshot, you can put it in the backgroud by `nohup wget -O geth.zip  "{paste snapshot URL here}" &`
- Uncompress: `unzip geth.zip`. It will take more than two hours to uncompress. You can put it in the backgroud by `nohup unzip geth.zip &`
- You can combine the above steps by running a script:
```
wget -O geth.zip  "{paste snapshot URL here}"
unzip geth.zip
```

Step 3: Replace Data
- First, stop the running bsc client if you have one by `kill {pid}`, and make sure the client has shut down.
- Consider backing up the original data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Start the bsc client again and check the logs

