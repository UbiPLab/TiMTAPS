# TiMTAPS
Threshold Signatures with Verifiably Timed Combining and Message-Dependent Tracing

# 📁 Project Structure
├── main.py # <br>
├── ATS.py # Accountable Threshold Signature<br>
├── Sig.py # Digital signature<br>
├── ElGamal.py # ElGamal encryptio<br>
├── IKEM.py # Identity Based Encryption<br>
├── NIZK.py # Non-interactive zero-knowledge proofs<br>
├── HTLP_ADD.py / HTLP_MUL.py # Homomorphic Time-Lock Puzzle<br>
├── isPrime.py # Prime number judgment<br>
├── pqcreate.py # Generation of prime numbers<br>
├── DataTest.py # Data testing<br>
├── Blockchain.py # Blockchain connection test<br>
├── TiMTAPS.py # TiMTAPS standard version<br>
├── TiMTAPS_Blockchain.py # TiMTAPS blockchain version<br>
├── contract/ # Solidity smart contracts<br>
│ ├── TiMTAPS_sol_TiMtaps_constract.abi<br>
│ └── TiMTAPS_sol_TiMtaps_constract.bin<br>
├── data/ # Intermediate data or results<br>
├── keystore/ # Ethereum key files<br>

# ⚙️ Environment & Dependencies

## Python

- Python 3.9
- Web3.py for Ethereum interaction

Install Python dependencies:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install web3
```

## System Requirements

Download link：https://geth.ethereum.org/
