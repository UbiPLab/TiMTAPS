# TiMTAPS
Threshold Signatures with Verifiably Timed Combining and Message-Dependent Tracing

# 📁 Project Structure
├── main.py # 
├── ATS.py # Accountable Threshold Signature
├── Sig.py # Digital signature
├── ElGamal.py # ElGamal encryptio
├── IKEM.py # Identity Based Encryption
├── NIZK.py # Non-interactive zero-knowledge proofs
├── HTLP_ADD.py / HTLP_MUL.py # Homomorphic Time-Lock Puzzle
├── isPrime.py # Prime number judgment
├── pqcreate.py # Generation of prime numbers
├── DataTest.py # Data testing
├── Blockchain.py # Blockchain connection test
├── TiMTAPS.py # TiMTAPS standard version
├── TiMTAPS_Blockchain.py # TiMTAPS blockchain version
├── contract/ # Solidity smart contracts
│ ├── TiMTAPS_sol_TiMtaps_constract.abi
│ └── TiMTAPS_sol_TiMtaps_constract.bin
├── data/ # Intermediate data or results
├── keystore/ # Ethereum key files

# ⚙️ Environment & Dependencies

## Python

- Python 3.9
- Web3.py for Ethereum interaction

Install Python dependencies:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install web3

## System Requirements

Download link：https://geth.ethereum.org/
