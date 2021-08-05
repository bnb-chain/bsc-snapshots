# bsc-snapshots

Pruned database:

[Bsc-20210804.zip](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20210804.zip?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Expires=1630723350&Signature=1aQFhpJDz6yygOMRuflUuk8F3jc%3D%3D) (size 362.0GB)

checksum: 4649caad90cbcf62a063e6fc4d368070

# Usage 

Step1: Preparation
- Make sure your hardware meets the [suggested requirement](https://docs.binance.org/smart-chain/developer/fullnode.html).
- A disk with enough free storage, atlest twice of the size of snapshot.

Step2: Download && Uncompress
- Copy the above snapshot URL.
- Download:  `wget -O geth.zip  "{paste snapshot URL here}"` . It will take one ro two hours to download the snaoshot, you can put it backgroud by `nohup wget -O geth.zip  "{paste snapshot URL here}" &`
- Uncompress: `unzip geth.zip`. It will take more than two hours to uncompress,  you can put it backgroud by `nohup unzip geth.zip &`
- You can combine above steps by running a script:
```
wget -O geth.zip  "{paste snapshot URL here}"
unzip geth.zip
```

Step3: Replace Data
- Stop the running bsc client first if you have one by `kill {pid}`, and make sure the client is shutdowned.
- Backup the origin data: `mv ${BSC_DataDir}/geth/chaindata ${BSC_DataDir}/geth/chaindata_backup; mv ${BSC_DataDir}/geth/triecache ${BSC_DataDir}/geth/triecache_backup`
- Replace the data: `mv server/data-seed/geth/chaindata ${BSC_DataDir}/geth/chaindata; mv server/data-seed/geth/triecache ${BSC_DataDir}/geth/triecache`
- Statr the bsc client again and check logs


