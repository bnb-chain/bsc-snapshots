
# bsc-snapshots

Pruned database:

### Asia endpoint:

[geth-20211031.tar.gz
](https://s3.ap-northeast-1.amazonaws.com/dex-bin.bnbstatic.com/geth-20211031.tar.gz?AWSAccessKeyId=AKIAYINE6SBQPUZDDRRO&Signature=ESK5xmr5f1AIK4Mr6our%2FALXzQk%3D&Expires=1638310885
)


### EU  endpoint:

[geth-20211101.tar.gz
](https://tf-dex-prod-public-snapshot.s3.amazonaws.com/geth-20211101.tar.gz?AWSAccessKeyId=ASIAYINE6SBQDD3BTBXG&Signature=SEcHy%2BzxzDFdRaJ6My0T63KTLWs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAL7W8TrAR5o4nRFwSxNi%2F3ADC2Nr0dKEnd23VLfqPGWxAiBjDOB2K3X5mgonGMcwdXCKl4q17GE%2Faqv0%2BauJ4%2BiWkSqEBAguEAIaDDU2NzgxODQ4OTk1MiIMF2ZTByaIM93Af5cVKuED6oVpNaBzSa%2F8Vhm5qiRgLKK3CNtBj%2F3V8p7x0ygh4XyUJF7vhtLfwiTXvdnA85kyN4LtwIjbF4MKBPX45KonaZw8u0h0K2XbT4NmWk6PhZ1iCv34chAvu59sxL1ORm2ecgFo1%2F9FCoqe2YIkWce0TjV7z7SDa7wNOyzYbWXoJQVRcwfffP3vIyiUbDfX3iM4A41GtONAyMJ84M0Abg6si3QN5C9izkYYC5rWfIsfUYwpNRS5fxRRvI5CvJdfqD2ORrtf4RG%2ByvpzrrGvvwYTMAgeiF5eHHKzqKQgqTsRtXpMy0%2FpHBjhekbTOvg1UvWos8eR%2FBStyRtZNOJXeE8Qtrkbtre97%2FIrIaQGVzhJOJPsqhfwEDD0p4%2BT4jzlvjAtnD7RaXvuDjUH3eDbxpBBfm82XhF3gUHI%2BBUDzzQIy2NLpqZqHMUJ1T2tiyvPLxARsbPFNX%2BxxUn3b8I6MQIwNWV96tin7cq6v1KSBL5MxjYhYhWaZFcM%2Fo4VNV22vxDGQ%2F2ar%2FuUnlqRFj0WPDP6uelPo%2FuaTvM5Qj95XRObg6QLplbiFyxqOEQW2upud%2FShP2qfvZxpEmcypi%2F%2BxHknh%2BmBAIqDKaTYjQFlXzFGJ4z3lXYX%2BlYIDiVROrkJT4zsKzDl8ISMBjqlAYdGz72Rt7KF8RhSXp1WdUEg8LE%2BAH8MHjONQIAm0v1zUNqAN%2FcDfOicoS4nAjX2oUqMKa9nHdy2%2FlyVN2Xg3Xt61kUyeFlZiKrOXMiQtGlAcwd3wLhBVNGOmDARrIxcG4nB18yA2Bzv7emBXNeAsBMUrzg5U3a2QJ7g5202QgNtTO6%2FYTaD%2FqRB%2F0bRpne4jRz4N%2B87wnHxCAeaNKtqNvDUYX7R5Q%3D%3D&Expires=1636466278
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

