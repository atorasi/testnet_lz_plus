from random import randint
from time import sleep

from config import SLEEP_ACCS, SLEEP_ACCS_FROM, SLEEP_ACCS_TO, SLEEP_AKTIVE, SLEEP_AKTIVE_TO, SLEEP_AKTIVE_FROM


def newersleep_accs() -> int:
    time = randint(SLEEP_ACCS_FROM, SLEEP_ACCS_TO) if SLEEP_ACCS else 0
    sleep(time)
    return time

def newersleep_aktiv() -> int:
    if SLEEP_AKTIVE:
        time = randint(SLEEP_AKTIVE_FROM, SLEEP_AKTIVE_TO)
        sleep(time)
    return time

