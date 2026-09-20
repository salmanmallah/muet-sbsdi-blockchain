# ⛓️ MUET SBSDI Blockchain Package

**Official Scalable Python Blockchain Package & Laboratory Implementations**  
*Mehran University of Engineering & Technology (MUET), Jamshoro*  
*Sindh Blockchain Skills Development Initiative (SBSDI) — Sindh Higher Education Commission (SHEC)*

---

[![University](https://img.shields.io/badge/Institution-MUET%20Jamshoro-0056b3.svg)](https://www.muet.edu.pk/)
[![Initiative](https://img.shields.io/badge/Program-SBSDI%20Sindh-28a745.svg)](#)
[![Status](https://img.shields.io/badge/Status-Under%20Active%20Development-orange.svg)](#)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Tests-19%2F19%20Passing-brightgreen.svg)](#)

---

## 🏛️ Overview

The **MUET SBSDI Blockchain Package** is a scalable, production-ready Python library designed for undergraduate coursework, practical laboratory experiments, and research under the **Sindh Blockchain Skills Development Initiative (SBSDI)** at **Mehran University of Engineering & Technology (MUET), Jamshoro**.

> [!IMPORTANT]
> **Active Development Notice:** This package is currently **under active development**. Modules and interfaces are continuously updated and expanded as additional laboratory exercises and advanced blockchain components are introduced.

### Key Capabilities & Highlights
* **Zero Dependency Conflicts:** Standardizes cryptographic primitives (`secp256k1` curves and Keccak-256) into a unified, conflict-free dependency set.
* **Modular & Scalable Design:** Easily extensible codebase organized by independent modules, allowing new algorithms and lab components to be added seamlessly.
* **Verified Reference Implementations:** 100% automated test-passing reference implementations for distributed ledgers, peer-to-peer networks, cryptographic hashing, and consensus protocols.

---

## 📦 Installation

Install the package directly in editable mode for development or via standard pip:

```bash
# Clone the repository
git clone https://github.com/salmanmallah/muet-sbsdi-blockchain.git
cd muet-sbsdi-blockchain

# Install in editable mode with dependencies
pip install -e .
```

### Core Dependencies
This package automatically installs and manages the following verified dependencies:
* `ecdsa>=0.18` — For SECP256k1 key generation, digital signatures, and verification.
* `pycryptodome>=3.15` — For Ethereum-compatible Keccak-256 cryptographic hashing.

> [!NOTE]
> If you have the legacy `pycrypto` library installed, please uninstall it first using `pip uninstall pycrypto` to avoid namespace collisions.

---

## 🔬 Practical Lab Modules & Examples

### Module 1: Blockchain Fundamentals & Proof-of-Work
*Covers block data structures, SHA-256 cryptographic chaining, block tampering detection, and proof-of-work difficulty benchmarking.*

```python
from sbsdi_blockchain.lab1 import Block, Blockchain, time_mining

# Initialize blockchain
chain = Blockchain()
chain.add_block("Alice transfers 5 coins to Bob", difficulty=4)
chain.add_block("Bob transfers 2 coins to Carol", difficulty=4)

# Validate chain integrity
print(f"Chain Valid: {chain.is_chain_valid()}")  # True

# Tamper simulation
chain.chain[1].data = "Alice transfers 5000 coins to Bob"
print(f"Tampered Chain Valid: {chain.is_chain_valid()}")  # False

# Benchmark mining execution time across difficulties
elapsed = time_mining(Blockchain(), "Benchmark Block", difficulty=4)
print(f"Mining elapsed time: {elapsed:.3f}s")
```

---

### Module 2: Distributed Ledgers & P2P Networks
*Covers distributed ledger synchronization, peer-to-peer gossip broadcast, Merkle tree integration, secp256k1 wallets, transaction lifecycles, and mempools.*

```python
from sbsdi_blockchain.lab2 import (
    DistributedLedgerNetwork,
    build_ring,
    Wallet,
    Transaction,
    Blockchain
)

# 1. Distributed Ledger Consistency
network = DistributedLedgerNetwork(["Node_A", "Node_B", "Node_C"])
network.broadcast_entry({"tx": "Alice sends 10"}, origin_node="Node_A")
print(f"Network Consistent: {network.is_consistent()}")  # True

# 2. P2P Gossip Protocol Simulation
nodes = build_ring(8)
nodes[0].broadcast("New block announced!")
print(f"Gossip Delivered to All: {all(len(n.inbox) == 1 for n in nodes)}")  # True

# 3. Wallets, Signed Transactions & Mempool
alice = Wallet("Alice")
bob = Wallet("Bob")

tx = Transaction(alice, bob.address(), amount=10.0, fee=0.5)
tx.sign()

bc = Blockchain(difficulty=4, genesis_grants={alice.address(): 100})
bc.submit_transaction(tx)
bc.mine_pending_transactions()
print(f"Chain Integrity: {bc.is_chain_valid()}")  # True
```

---

### Module 3: Cryptographic Foundations & Ethereum Primitives
*Covers SHA-256 avalanche effect, Keccak-256, ECDSA keypair generation, Ethereum address derivation (0x + 40 hex chars), and Merkle SPV inclusion proofs.*

```python
from sbsdi_blockchain.lab3 import (
    sha256,
    keccak256,
    generate_keypair,
    sign,
    verify,
    derive_eth_address,
    MerkleTree,
    verify_proof
)

# 1. Cryptographic Hashing
print("SHA-256:", sha256(b"MUET SBSDI"))
print("Keccak-256:", keccak256(b"MUET SBSDI"))

# 2. Key Generation & Digital Signatures
priv, pub = generate_keypair()
msg = b"Transfer 50 ETH to Research Pool"
sig = sign(priv, msg)
print(f"Signature Valid: {verify(pub, sig, msg)}")  # True

# 3. Ethereum Address Derivation
eth_address = derive_eth_address(pub)
print(f"Derived Address: {eth_address}")

# 4. Merkle Tree & SPV Proof Verification
transactions = [b"tx0", b"tx1", b"tx2", b"tx3"]
tree = MerkleTree(transactions)
proof = tree.get_proof(index=2)

print(f"Merkle Root: {tree.root()}")
print(f"SPV Proof Valid: {verify_proof(transactions[2], proof, tree.root())}")  # True
```

---

### Module 4: Consensus Mechanisms & Network Metrics
*Covers Proof-of-Stake (PoS), validator selection, slashing conditions, Practical Byzantine Fault Tolerance (PBFT $2f+1$ quorum), Nakamoto coefficient calculation, and sharded TPS metrics.*

```python
from sbsdi_blockchain.lab4 import (
    PoWBlockchain,
    Validator,
    select_validator,
    slash,
    build_network,
    pbft_consensus,
    nakamoto_coefficient,
    calculate_tps,
    pbft_message_count,
    sharded_tps
)

# 1. Proof of Stake & Slashing
validators = [
    Validator("MUET_Pool_A", stake=300),
    Validator("MUET_Pool_B", stake=200),
    Validator("MUET_Pool_C", stake=100),
]
leader = select_validator(validators)
print(f"Elected Block Proposer: {leader.name}")

slash(validators[0], penalty=0.5)
print(f"Slashed State: {validators[0].slashed}, New Stake: {validators[0].stake}")

# 2. PBFT Consensus (3-Phase Simulation)
# n=7, f=2 Byzantine faults tolerated, quorum=5
nodes = build_network(7, num_byzantine=2)
result = pbft_consensus(nodes, "COMMIT_BLOCK_42")
print(f"PBFT Consensus Reached: {result['consensus_reached']}")

# 3. Decentralization & Scalability Metrics
hash_distribution = [25, 20, 15, 12, 10, 8, 6, 4]
print(f"Nakamoto Coefficient: {nakamoto_coefficient(hash_distribution)}")

print(f"Theoretical Bitcoin TPS: {calculate_tps(1_000_000, 250, 600):.2f}")
print(f"PBFT Messages (n=7): {pbft_message_count(7)}")
print(f"Sharded Network TPS (64 shards): {sharded_tps(7, 64):.1f}")
```

---

## 🗂️ Package Directory Structure

```text
sbsdi_blockchain/
├── __init__.py
├── core/
│   ├── __init__.py
│   └── hashing.py          # Shared hashing primitives (sha256, sha256d, keccak256)
├── lab1/
│   ├── __init__.py
│   ├── block.py            # Block data structure
│   ├── blockchain.py       # Blockchain ledger & validation
│   └── pow.py              # Mining benchmarks & difficulty analysis
├── lab2/
│   ├── __init__.py
│   ├── dlt.py              # Distributed Ledger Network
│   ├── p2p.py              # Peer-to-peer gossip protocol
│   ├── merkle.py           # Merkle root calculation
│   ├── block.py            # Merkle-enabled block representation
│   ├── wallet.py           # secp256k1 cryptographic wallet
│   ├── transaction.py      # Signed transaction lifecycle
│   ├── mempool.py          # Transaction pool & balance accounting
│   ├── blockchain.py       # Transaction-enabled blockchain
│   └── consensus.py        # Longest-chain consensus simulation
├── lab3/
│   ├── __init__.py
│   ├── sha256_basics.py    # SHA-256 & avalanche effect tests
│   ├── keccak256.py        # Keccak-256 implementation
│   ├── pow.py              # Standalone proof-of-work algorithm
│   ├── ecdsa_keys.py       # SECP256k1 key generation
│   ├── eth_address.py      # Ethereum public key to address derivation
│   ├── sign_verify.py      # Digital signatures & message verification
│   ├── merkle.py           # MerkleTree & SPV inclusion proofs
│   └── capstone.py         # Capstone mini-blockchain
└── lab4/
    ├── __init__.py
    ├── pow.py              # Advanced PoW blockchain
    ├── pos.py              # Proof-of-Stake with validator slashing
    ├── pbft.py             # Practical Byzantine Fault Tolerance
    ├── decentralization.py # Nakamoto coefficient metrics
    └── scalability.py      # Block size, propagation & TPS calculations
```

---

## 🎓 Academic Affiliation & Credits

* **Academic Institution:** [Mehran University of Engineering & Technology (MUET)](https://www.muet.edu.pk/), Jamshoro, Sindh, Pakistan
* **Initiative:** Sindh Blockchain Skills Development Initiative (SBSDI)
* **Sponsoring Body:** Sindh Higher Education Commission (SHEC), Government of Sindh
* **License:** [MIT License](LICENSE)
