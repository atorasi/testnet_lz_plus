from random import randint
from time import sleep

from core import check_balance, bridge_to_geth, bridge_geth_scroll
from utils import logger, newersleep_accs, newersleep_aktiv, success_accs_w
from config import *


with open('private_keys.txt') as file:
    keys = [key.strip() for key in file]
    
    
def main():
    for acc_num, key in enumerate(keys, start=1):
        acc_info = f'|-{acc_num}-|-{key[:3]}. . .{key[-3:]}-|'
        
        balance_op = check_balance(key, RPC['optimism'])
        logger.info(f'{acc_info} Optimism ETH Balance: {balance_op}')
        
        balance_arb = check_balance(key, RPC['arbitrum'])
        logger.info(f'{acc_info} Arbitrum ETH Balance: {balance_arb}')
        
        balance_geth = temp_geth = check_balance(key, RPC['goerli'])

        main_chain = 'arbitrum' if balance_arb > balance_op else 'optimism'
        balance_to_lz = balance_arb if main_chain == 'arbitrum' else balance_op
        
        temp_lz_value = balance_to_lz * randint(MIN_PERCENT_LZ * 1_000, MAX_PERCENT_LZ * 1_000) / 100_000
        value_to_lz = temp_lz_value if USE_PERCENT == True and temp_lz_value > 0.0002 else randint(20 * 1_000, 30 * 1_000) / 100_000_000
        
        logger.info(f'{acc_info} Перевожу {value_to_lz} из сети {main_chain}')
        bridge_lz_hash = bridge_to_geth(key, RPC[main_chain], value_to_lz)
        
        logger.success(f"{acc_info} Transaction: https://arbiscan.io/tx/{bridge_lz_hash}") if main_chain == 'arbitrum' else (f"{acc_info} Transaction: https://optimistic.etherscan.io/tx/{bridge_lz_hash}")
        logger.info(f'Сплю {newersleep_aktiv()} секунд между активностями')
        
        logger.info(f'{acc_info} Жду поступления средств в Goerli')
        while temp_geth == balance_geth:
            balance_geth = check_balance(key, RPC['goerli'])
            sleep(3)
        logger.success(f'{acc_info} Средства поступили на счет, Goerli ETH Balance: {balance_geth}')
    
        temp_to_scroll = balance_geth * randint(MIN_PERCENT_GETH * 1_000, MAX_PERCENT_GETH * 1000) / 100_000
        
        logger.info(f'{acc_info} Бриджу {temp_to_scroll} gETH в SCROLL')
        scroll_tx = bridge_geth_scroll(key, RPC['goerli'], temp_to_scroll)
        
        logger.success(f"{acc_info} Transaction: https://goerli.etherscan.io/tx/{scroll_tx}")       
        success_accs_w(key)
        
        logger.info(f'><><><>< Сплю {newersleep_accs()} секунд перед следующим аккаунтом ><><><><')
        
        
if __name__ == '__main__':
    print(TEXT)
    main()
    while True:
        print('Спасибо что воспользовались софтом!\nhttps://t.me/tripleshizu')
        sleep(1)
        
        
        

        
        
