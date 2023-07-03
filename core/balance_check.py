from web3 import Web3

from utils import script_exceptions

@script_exceptions
def check_balance(key: str, rpc: str) -> float:
    w3 = Web3(Web3.HTTPProvider(rpc))
    acc = w3.eth.account.from_key(key)
    balance = w3.eth.get_balance(acc.address)
    return float(w3.from_wei(balance, 'ether'))