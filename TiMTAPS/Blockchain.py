from web3 import Web3, HTTPProvider
import json


# 获取合约的字节码和 ABI
with open('TiMtaps_sol_TiMtaps_constract.abi', 'r') as f:
    abi = json.load(f)

with open('TiMtaps_sol_TiMtaps_constract.bin', 'r') as f:
    bytecode = f.read()

# 连接到本地 Geth 节点
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 确保连接成功
if not w3.is_connected():
    print("Failed to connect to Ethereum node")


# 获取默认账户
default_account = w3.eth.accounts[0]
# 部署合约
SignatureVerifier = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = SignatureVerifier.constructor().transact({'from': default_account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")
# 创建合约实例
contract = w3.eth.contract(address=contract_address, abi=abi)

def call_contract():
    try:
        # 调用状态改变函数
        test = 'everybody love themselves'
        account = w3.eth.accounts[0]  # 使用第一个账户
        tx_hash = contract.functions.setsigma_cor(test).transact({'from': account})

        # 等待交易被处理
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print('Transaction successful with hash:', tx_hash.hex())

        # 调用只读函数
        current_value = contract.functions.getsigma_cor().call()
        print('Current value:', current_value)

    except Exception as e:
        print('Error calling contract:', e)

call_contract()