
# 1.Mode-1: Hash&LevelDB mode
If you need Hash based snapshot, check out [FAQ-Q2](https://github.com/bnb-chain/bsc-snapshots/issues/349)

# 2.Mode-2: Multi-Database(experimental feature)**
## 2.1.About Snapshot with multi-database
Multi-databases are a new feature in [bsc v1.4.6](https://github.com/bnb-chain/bsc/releases/tag/v1.4.6).

The Chaindata of the snapshot will be divided into three stores, BlockStore, TrieStore, and OriginalStore.

TrieStore: All trie nodes of the current state and historical state data of nearly 9w blocks are stored here. The data is stored in  ${BSC_DataDir}/geth/chaindata/state.

BlockStore: Block-related data is stored in this store, including headers, bodies, receipts, difficulties, number-to-hash indexes, hash-to-number indexes,
and historical block data. The data is stored in ${BSC_DataDir}/geth/chaindata/block.

If the user intends to store the databases on the same storage disk, they just need to start the client by following the same steps after extracting the snapshot file, without requiring any additional startup parameters.

If the user want to store different databases on different disks, you can move the folder corresponding to TrieStore or BlockStore to a different directory and create a symbolic link with the same name as the folder using an absolute path in the chaindata directory.
For example:
```
mv ${BSC_DataDir}/geth//chaindata/state <move-directory>
ln -s <move-directory>  ${BSC_DataDir}/geth/chaindata/state
```
After the symbolic link is created, you can start the bsc client again and check the logs.
Due to the larger size of the trie store, we recommend that the trie database be stored on different disks to achieve better performance.

## 2.2.Endpoints
When the user runs node with the new snapshot of the multi-databases below, the feature will be enabled automatically.

- mainnet: [geth-pbss-multidatabase-20240620.tar.lz4](https://pub-c0627345c16f47ab858c9469133073a8.r2.dev/geth-pbss-multidatabase-20240620.tar.lz4)(md5: 8333e762e72a590dca6cb46daeffa279)


