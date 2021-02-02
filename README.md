# btc

Few basic functionality implementation to ensure understanding of blockchain.
1. ec.py: basic elliptic curve point operation like point addition, point doubling, point substraction etc
      1.1 ECadd(): elliptic curve point addition
      1.2 ECdoubling(): elliptic curve point doubling      
      1.3 ECsub(): elliptic curve point substraction
      
2. verify_btc_block.py : Verification of bitcoin block hash. That includes
      2.1 markle root calculation: root hash of the markle tree from all the transaction hash included in the specified block.
      2.2 hash generation: generation of block hash from version, previous block hash, markle root hash, timestamp, bits and nonce.

