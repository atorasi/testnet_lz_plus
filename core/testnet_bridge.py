from web3 import Web3
from random import randint

from utils import abi_read, script_exceptions


@script_exceptions
def bridge_to_geth(key: str, rpc: str, value: float) -> hex:
    w3 = Web3(Web3.HTTPProvider(rpc))
    acc = w3.eth.account.from_key(key)
    address = acc.address
    contract_instance = w3.eth.contract(address='0x0A9f824C05A74F577A536A8A0c673183a872Dff4', abi=abi_read('abies\\bridge_testnet.json'))
    tx = contract_instance.functions.swapAndBridge(
        w3.to_wei(value, 'ether'), 
        w3.to_wei(value, 'ether')* randint(6000, 7900),
        154,
        address,
        address,
        '0x0000000000000000000000000000000000000000',
        b'',    
    ).build_transaction({
        'from': acc.address,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(acc.address),
        'value': w3.to_wei(0.000161938112081064, 'ether') + w3.to_wei(value, 'ether')
    })
    
    sign = acc.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(sign.rawTransaction)
    reciept = w3.eth.wait_for_transaction_receipt(tx_hash)

    return w3.to_hex(tx_hash)