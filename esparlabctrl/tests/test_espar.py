import pytest
from esparlabctrl.espar_lab import Espar
import time


def test_espar_sct():
    espar = Espar()
    t1 = time.time()
    per, rssi = espar.test_char(0)
    print(f"CHAR 0: per={per}, rssi={rssi}")
    # print(f"CHAR 1415: {espar.test_char(1415)}")
    per, rssi = espar.test_char(1415)
    print(f"CHAR 1415: per={per}, rssi={rssi}")
    # print(f"CHAR 1754: {espar.test_char(1754)}")
    per, rssi = espar.test_char(1754)
    print(f"CHAR 1754: per={per}, rssi={rssi}")
    # print(f"CHAR 4095: {espar.test_char(4095)}")
    per, rssi = espar.test_char(4095)
    print(f"CHAR 4095: per={per}, rssi={rssi}")
    t2 = time.time()
    print(f"Time: {t2-t1}")
