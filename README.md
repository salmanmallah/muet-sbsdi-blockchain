<p align="center">
  <img src="assets/sindh_hec_logo.svg" alt="Sindh Higher Education Commission Logo" width="120" height="120">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/muet_logo.svg" alt="MUET Jamshoro Logo" width="120" height="120">
</p>

<h1 align="center">⛓️ MUET SBSDI Blockchain Package</h1>

<p align="center">
  <strong>Official Scalable Python Blockchain Reference Package & Laboratory Implementations</strong><br>
  <em>Mehran University of Engineering & Technology (MUET), Jamshoro</em><br>
  <em>Sindh Blockchain Skills Development Initiative (SBSDI) — Sindh Higher Education Commission (SHEC)</em>
</p>

<p align="center">
  <a href="https://www.muet.edu.pk/"><img src="https://img.shields.io/badge/Institution-MUET%20Jamshoro-0056b3.svg" alt="Institution"></a>
  <a href="#"><img src="https://img.shields.io/badge/Program-SBSDI%20Sindh-28a745.svg" alt="Program"></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Under%20Active%20Development-orange.svg" alt="Status"></a>
  <a href="#"><img src="https://img.shields.io/badge/PyPI-Publishing%20Soon-yellow.svg" alt="PyPI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
  <a href="https://github.com/salmanmallah/muet-sbsdi-blockchain/actions"><img src="https://github.com/salmanmallah/muet-sbsdi-blockchain/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

---

## 🏛️ Overview

The **MUET SBSDI Blockchain Package** is a scalable, production-grade Python library designed for undergraduate coursework, laboratory instruction, and hands-on experiments under the **Sindh Blockchain Skills Development Initiative (SBSDI)** at **Mehran University of Engineering & Technology (MUET), Jamshoro**.

> [!IMPORTANT]
> **Active Development & PyPI Roadmap:**  
> * **Active Development:** This package is continuously updated as new laboratory modules and blockchain algorithms are introduced.  
> * **PyPI Release:** The package will soon be published to the official Python Package Index (PyPI) for direct `pip install` access. Currently, students and researchers can install and use it directly via GitHub as shown below.

### Key Highlights
* **Zero Dependency Conflicts:** Standardizes cryptographic primitives (`secp256k1` curves and Keccak-256) into a unified, conflict-free dependency set.
* **Modular & Scalable Design:** Organized into independent modules, allowing new consensus algorithms, cryptographic tools, and lab exercises to be added seamlessly.
* **100% Verified Reference Implementations:** All modules are thoroughly tested with automated verification for distributed ledgers, P2P networking, hashing, and consensus protocols.

---

## 🚀 Quickstart Guide for Students

Follow these simple steps to install and start using the package in your Python scripts or Jupyter Notebooks.

### Step 1: Install the Package

You can install the package directly into your Python environment using either of the two methods below:

#### Option A: Direct One-Line Install from GitHub (Recommended)
```bash
pip install git+https://github.com/salmanmallah/muet-sbsdi-blockchain.git
```

#### Option B: Clone for Local Development (Editable Mode)
```bash
# 1. Clone the repository
git clone https://github.com/salmanmallah/muet-sbsdi-blockchain.git
cd muet-sbsdi-blockchain

# 2. Install in editable mode (auto-installs all required dependencies)
pip install -e .
```

*(Note: Once published to PyPI, you will be able to simply run `pip install muet-sbsdi-blockchain`)*

---

### Step 2: Create Your Python Script or Notebook

Create a new file (e.g., `main.py` or a Jupyter notebook `experiment.ipynb`) and import the required modules directly into your project!

```python
# Example: Create and mine your first blockchain block
from sbsdi_blockchain.lab1 import Blockchain

my_blockchain = Blockchain()
my_blockchain.add_block(data="Transfer 10 MUET-Coins to Student A", difficulty=4)

print("Block Successfully Mined!")
print("Chain Valid:", my_blockchain.is_chain_valid())
```

---

## 🔬 Practical Lab Modules & Code Examples

### Module 1: Blockchain Fundamentals & Proof-of-Work
*Covers block data structures, SHA-256 cryptographic chaining, block tampering detection, and proof-of-work difficulty benchmarking.*

```python
from sbsdi_blockchain.lab1 import Block, Blockchain, time_mining

# 1. Initialize blockchain and add mined blocks
chain = Blockchain()
chain.add_block("Alice transfers 5 coins to Bob", difficulty=4)
chain.add_block("Bob transfers 2 coins to Carol", difficulty=4)

# 2. Validate chain integrity
print(f"Chain Valid: {chain.is_chain_valid()}")  # True

# 3. Tamper simulation (tampering invalidates the cryptographic chain)
chain.chain[1].data = "Alice transfers 5000 coins to Bob"
print(f"Tampered Chain Valid: {chain.is_chain_valid()}")  # False

# 4. Benchmark mining execution time across difficulties
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

# 1. Distributed Ledger Consistency & Sync
network = DistributedLedgerNetwork(["Node_A", "Node_B", "Node_C"])
network.broadcast_entry({"tx": "Alice sends 10"}, origin_node="Node_A")
print(f"Network Consistent: {network.is_consistent()}")  # True

# 2. P2P Gossip Protocol Simulation (8-node ring topology)
nodes = build_ring(8)
nodes[0].broadcast("New block announced!")
print(f"Gossip Delivered to All: {all(len(n.inbox) == 1 for n in nodes)}")  # True

# 3. Cryptographic Wallets & Signed Transactions
alice = Wallet("Alice")
bob = Wallet("Bob")

# Alice signs transaction with ECDSA private key
tx = Transaction(alice, bob.address(), amount=10.0, fee=0.5)
tx.sign()

# Submit to blockchain mempool and mine
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

# 2. Key Generation & Digital Signatures (secp256k1)
priv, pub = generate_keypair()
msg = b"Transfer 50 ETH to Research Pool"
sig = sign(priv, msg)
print(f"Signature Valid: {verify(pub, sig, msg)}")  # True

# 3. Ethereum Address Derivation (Keccak-256 of uncompressed public key)
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

# 1. Proof of Stake & Validator Slashing
validators = [
    Validator("MUET_Pool_A", stake=300),
    Validator("MUET_Pool_B", stake=200),
    Validator("MUET_Pool_C", stake=100),
]
leader = select_validator(validators)
print(f"Elected Block Proposer: {leader.name}")

slash(validators[0], penalty=0.5)
print(f"Slashed State: {validators[0].slashed}, New Stake: {validators[0].stake}")

# 2. PBFT Consensus Simulation (3-Phase: Pre-prepare, Prepare, Commit)
# Network of 7 nodes, tolerating f=2 Byzantine faulty nodes (Quorum = 5)
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
