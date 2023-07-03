from web3 import Web3

from utils import logger, abi_read, script_exceptions


@script_exceptions
def bridge_geth_scroll(private_key: str, rpc: str, value: float) -> str:
    #Бридж gETH ----> SCROLL
    w3 = Web3(Web3.HTTPProvider(rpc))
    if w3.is_connected():
        acc = w3.eth.account.from_key(private_key)
        adres = acc.address
        contract_instance = w3.eth.contract(address='0xe5E30E7c24e4dFcb281A682562E53154C15D3332', abi=abi_read("abies\goerli_scroll.json"))

        tx = contract_instance.functions.depositETH(w3.to_wei(value, 'ether'), 40000).build_transaction({
            "gasPrice": w3.eth.gas_price,
            "from": adres,
            "nonce": w3.eth.get_transaction_count(adres),
            "value": w3.to_wei(value, 'ether') + w3.to_wei(0.00000004, 'ether'),
        })
        
        sign = acc.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(sign.rawTransaction)

        
        return w3.to_hex(tx_hash)