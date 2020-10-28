# btc

Few basic functionality implementation to ensure understanding of blockchain.
1. verify_btc_block.py : Verification of bitcoin block hash. That includes

      1.1 markle root calculation: root hash of the markle tree from all the transaction hash included in the specified block.
      
      1.2 hash generation: generation of block hash from version, previous block hash, markle root hash, timestamp, bits and nonce.
