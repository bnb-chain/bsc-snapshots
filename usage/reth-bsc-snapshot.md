# BSC Reth Client Snapshot Usage

## About BSC Reth client snapshot

Currently, snapshots are available for archive node configurations of the BSC Reth client. Please note that as the client is in active development, snapshot updates do not follow a fixed schedule and will be released as they become available.

The Snapshot for BSC mainnet fullnode configuration will be released soon.

## Building from Source

To build the optimized `reth-bsc` binary from source:

```bash
RUSTFLAGS="-C target-cpu=native" cargo build --profile maxperf --features jemalloc,asm-keccak
```

**Build options explained:**
- `RUSTFLAGS="-C target-cpu=native"`: Optimizes for your specific CPU architecture
- `--profile maxperf`: Uses the maximum performance build profile
- `--features jemalloc`: Uses jemalloc allocator for better memory performance
- `--features asm-keccak`: Uses assembly-optimized Keccak implementation

After building, the binary will be located at `./target/maxperf/reth-bsc`.

## Snapshots Download link

> **Note**: BSC MainNet Archive node snapshot is split into two parts for easier download. Both files are required for a complete archive node setup.

**Snapshots**

All reth-bsc snapshots are moved to [BSC Reth Snapshots](https://github.com/bnb-chain/bsc-snapshots#source-4-bsc-reth-snapshots) to download.

## Installation Instructions

### BSC MainNet Archive Node Setup

After downloading both snapshot files, follow these steps to set up your archive node:

1. **Create your data directory** (if it doesn't exist):
   ```bash
   mkdir -p /path/to/your/reth-data-dir
   cd /path/to/your/reth-data-dir
   ```

2. **Extract the static files**:
   ```bash
   zstd -d -T0 --long=31 -c reth_static_files_20251126.tar.zst | tar -xvf -
   # This will create/populate the 'static_files' directory
   ```

3. **Extract the database files**:
   ```bash
   zstd -d -T0 --long=31 -c reth_db_20251126.tar.zst | tar -xvf -
   # This will create/populate the 'db' directory
   ```

4. **Verify the directory structure**:
   Your data directory should contain:
   ```
   ├── db/                # Database files (from reth_db.tar.zst)
   ├── static_files/      # Static files (from reth_static_files.tar.zst)
   ├── blobstore/         # Will be created during runtime
   ├── logs/              # Will be created during runtime
   ├── parlia_snapshots/  # Will be created during runtime
   └── other runtime directories...
   ```

5. **Start your BSC Reth archive node**:

   Production-ready command with recommended settings:
   ```bash
   RUST_LOG=info reth-bsc node \
       --chain=bsc \
       --datadir=/path/to/your/reth-data-dir \
       --trusted-peers=enode://551c8009f1d5bbfb1d64983eeb4591e51ad488565b96cdde7e40a207cfd6c8efa5b5a7fa88ed4e71229c988979e4c720891287ddd7d00ba114408a3ceb972ccb@34.245.203.3:30311,enode://c637c90d6b9d1d0038788b163a749a7a86fed2e7d0d13e5dc920ab144bb432ed1e3e00b54c1a93cecba479037601ba9a5937a88fe0be949c651043473c0d1e5b@34.244.120.206:30311,enode://bac6a548c7884270d53c3694c93ea43fa87ac1c7219f9f25c9d57f6a2fec9d75441bc4bad1e81d78c049a1c4daf3b1404e2bbb5cd9bf60c0f3a723bbaea110bc@3.255.117.110:30311,enode://94e56c84a5a32e2ef744af500d0ddd769c317d3c3dd42d50f5ea95f5f3718a5f81bc5ce32a7a3ea127bc0f10d3f88f4526a67f5b06c1d85f9cdfc6eb46b2b375@3.255.231.219:30311,enode://5d54b9a5af87c3963cc619fe4ddd2ed7687e98363bfd1854f243b71a2225d33b9c9290e047d738e0c7795b4bc78073f0eb4d9f80f572764e970e23d02b3c2b1f@34.245.16.210:30311,enode://41d57b0f00d83016e1bb4eccff0f3034aa49345301b7be96c6bb23a0a852b9b87b9ed11827c188ad409019fb0e578917d722f318665f198340b8a15ae8beff36@34.245.72.231:30311,enode://1bb269476f62e99d17da561b1a6b0d0269b10afee029e1e9fdee9ac6a0e342ae562dfa8578d783109b80c0f100a19e03b057f37b2aff22d8a0aceb62020018fe@54.78.102.178:30311,enode://3c13113538f3ca7d898d99f9656e0939451558758fd9c9475cff29f020187a56e8140bd24bd57164b07c3d325fc53e1ef622f793851d2648ed93d9d5a7ce975c@34.254.238.155:30311,enode://d19fd92e4f061d82a92e32d377c568494edcc36883a02e9d527b69695b6ae9e857f1ace10399c2aee4f71f5885ca3fe6342af78c71ad43ec1ca890deb6aaf465@34.247.29.116:30311,enode://c014bbf48209cdf8ca6d3bf3ff5cf2fade45104283dcfc079df6c64e0f4b65e4afe28040fa1731a0732bd9cbb90786cf78f0174b5de7bd5b303088e80d8e6a83@54.74.101.143:30311 \
       --authrpc.addr "0.0.0.0" \
       --authrpc.port 8551 \
       --engine.parallel-sparse-trie \
       --http \
       --http.addr "0.0.0.0" \
       --http.port 8545 \
       --ws \
       --ws.addr "0.0.0.0" \
       --metrics 0.0.0.0:6060 \
       --http.api "admin, debug, eth, net, trace, txpool, web3, rpc, reth, ots"
   ```
   
   **Key parameters explained:**
   - `--engine.parallel-sparse-trie`: Enables parallel trie processing for better performance
   - `--trusted-peers`: BSC mainnet trusted peer nodes for faster syncing
   - `--http.api`: Enabled RPC API modules (add/remove as needed)

### Other Snapshots (TestNet/FullNode) Setup

For single-file snapshots (TestNet Archive, TestNet FullNode):

1. **Download and extract the snapshot**:
   ```bash
   mkdir -p /path/to/your/reth-data-dir
   cd /path/to/your/reth-data-dir
   
   # Extract the complete snapshot
   tar -xzf bsc-reth-*.tar.gz
   ```

2. **Start your node**:
   ```bash
   # For TestNet
   reth-bsc node --datadir /path/to/your/reth-data-dir --chain bsc-testnet
   
   # For MainNet FullNode (when available)
   reth-bsc node --datadir /path/to/your/reth-data-dir --chain bsc
   ```

### Requirements

- **Disk Space**: 
  - MainNet Archive: ~20TB+ free space
  - MainNet FullNode: ~8TB+ free space
  - TestNet Archive: ~1.5TB+ free space  
  - TestNet FullNode: ~900GB+ free space
- **Tools**: `zstd` (for .zst files), `tar`, `gzip` (for .tar.gz files)
- **Network**: Stable internet connection for large file downloads

> **Note**: Make sure you have sufficient disk space and the required decompression tools installed on your system.
