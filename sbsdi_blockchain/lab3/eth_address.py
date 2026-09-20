"""
sbsdi_blockchain.lab3.eth_address
===================================
Lab 3 (Lecture 4) — Section 5: Ethereum Address Derivation.

Source: 4_dis_blockchain_crypto_foundations_handout.docx, address_derivation.py
Dependencies: pycryptodome>=3.15, ecdsa>=0.18

Ethereum addresses are derived as: Keccak-256(uncompressed_public_key)[-20 bytes]
The public key used is the raw 64-byte uncompressed key (x || y),
WITHOUT the 0x04 prefix byte.
"""


def derive_eth_address(public_key) -> str:
    """
    Derive an Ethereum-style address from an ecdsa VerifyingKey.

    Algorithm:
    1. Get 64-byte uncompressed pubkey: x-coord (32 bytes) || y-coord (32 bytes)
    2. Keccak-256 hash the 64 bytes
    3. Take the LAST 20 bytes (40 hex chars) — that is the address


    Args:
        public_key: ecdsa.VerifyingKey (from generate_keypair() or Wallet.public_key)

    Returns:
        "0x" + 40-character hex string (Ethereum address format)

    Example:
        >>> from sbsdi_blockchain.lab3 import generate_keypair, derive_eth_address
        >>> priv, pub = generate_keypair()
        >>> addr = derive_eth_address(pub)
        >>> addr.startswith("0x")
        True
        >>> len(addr)
        42
    """
    from Crypto.Hash import keccak  # pycryptodome
    pub_bytes = public_key.to_string()  # 64-byte uncompressed pubkey (no 0x04 prefix)
    k = keccak.new(digest_bits=256)
    k.update(pub_bytes)
    address = k.hexdigest()[-40:]  # last 20 bytes
    return "0x" + address
