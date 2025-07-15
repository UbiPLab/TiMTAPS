import json

from web3 import Web3

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
if not w3.is_connected():
    print("Failed to connect to Ethereum node")

# 获取合约的字节码和 ABI
with open('TiMtaps_sol_TiMtaps_constract.abi', 'r') as f:
    contract_abi = f.read()

with open('TiMtaps_sol_TiMtaps_constract.bin', 'r') as f:
    bytecode = f.read()
# 获取默认账户
default_account = w3.eth.accounts[0]
# 部署合约
SignatureVerifier = w3.eth.contract(abi=contract_abi, bytecode=bytecode)
tx_hash = SignatureVerifier.constructor().transact({'from': default_account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")
# 创建合约实例
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 设置交易参数
transaction = {
    'from': default_account,
    'gas': 2000000,
    'gasPrice': w3.to_wei('20', 'gwei'),
    'nonce': w3.eth.get_transaction_count(default_account),
}
# callable_functions = dir(contract.functions)
# print(callable_functions)
# 调用合约方法
# 调用状态变更函数
try:
    param = "your_transaction_data"  # 替换为实际参数
    function_call = contract.functions.setsigma_cor(param)
    print(type(function_call))
    # 确保函数调用后使用 buildTransaction
    tx = function_call.transact(transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)  # 打印交易回执
    current_value = contract.functions.getsigma_cor().call()
    print('Current value:', current_value)
except AttributeError as e:
    print(f"Error calling contract: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")