
# bsc-snapshots

Pruned database:

### Asia endpoint:

[geth-20211031.tar.gz
](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20211031.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=ESK5xmr5f1AIK4Mr6our%2FALXzQk%3D&Expires=1638310885
)


### EU  endpoint:

[geth-20211031.tar.gz
](https://tf-dex-prod-public-snapshot.s3.amazonaws.com/geth-20211101.tar.gz?AWSAccessKeyId=ASIAYINE6SBQBN3ZKZBP&Signature=YrHwafdct5vPnEgx8nYNVD0EFkE%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH8aDmFwLW5vcnRoZWFzdC0xIkgwRgIhAImyNINfyCk82F%2BAZ4kzsJg%2Bt7FnUKsbojxY1%2BDeVqorAiEA4HxgdjcSjPWctmkGe0R9pnqVa2g6wVzRC4eva0wHhHYqhAQIKBACGgw1Njc4MTg0ODk5NTIiDLtRQ796wVs7VaDenirhAzAszyOgH07NmK3hF%2Fi1y70MEY%2BeIFfAsPnkwMaIWzggSVraDQYoK%2BkrfUMERxzrMcxa5FcWD%2F7G20nAm%2Bfi9NJ34aaSxUm64tQ72bPBIOv9K0SmNA%2Bg7W2hNA3DO49qWXANqaBhkCIoxC0e28vde1AfaXHqrIH5WH8%2BJQ2T47jQPfRftSpyr5JsdrGhwYoIAi6tkUHtKv9BUA0PwsqY64RedQ8SNrkJ12a8jrWj9%2FMBus3wkqNBZce9UK66pjS%2FV0%2B19V9INzEmrNobErPibtjp58XlH9oCyTPMxNQplVj2tgdcVhJAA2qac00rYFr9r10tBHWoL%2FzRZVmaE0e7q%2BQChveEUsAsAW3awuABAjvdfGZ9OiVA1%2BiwC9VeidVofLfeW48aYSweFSe8%2FD87oGKc8xI%2Bzi6kOG0M8KHzzJOY6%2FNROf%2B3aGxoqiRX6DafI0WHSoK1GJ0uUaKSU2RnjCfLvOOnE9NN0FNUIridwxnOFQWycv0wG1wRPL49emcAjDSep%2BHW2OTEkE0hTsiE4ryQ3%2F%2BSWhjxkB8XAYvIUmg%2FsAYOv1KMfMfsZMlzKL6F6%2Bf63pgP%2Fp1O6MhRa%2Fo5J8Ffcrmcz32%2B%2FWpFTVahmnrWaWNcwyR%2F8bW420bohUvz8YIw98WDjAY6pAG6D4P2ExbxZIUjRVw8ze04NxgJovWcz5bIR5t8UvMr9bE8HhyTXNXN%2BrFjKifLLHYySeUn6CaPJYCHsD4lUY5xzCiLqOF32tEun2jdN1r4y4U67Mb4cKe2zEp8pM64BGjvVBpUM0Lil2LjrJEtNcGtsemPjLaSeyb7pUHjsiE%2F4MTDh7Y1i1koBDLuuP5LnMwTa%2BO5UfMrchYBkz52oxNRddUuFg%3D%3D&Expires=1638429443
)

MD5 checksum: 8a297c7da61b4cf831b4c90e2af3ea9c



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

