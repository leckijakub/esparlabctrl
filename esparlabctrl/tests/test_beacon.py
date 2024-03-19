import pytest
from esparlabctrl import Beacon, BeaconState, BeaconConfig

from esparlabctrl.espar_lab import network as net
from paramiko import SSHClient

TEST_BEACON_IP = "192.168.0.1"
TEST_BEACON_ID = 0

@pytest.mark.mock
def test_create_beacon_mock(monkeypatch):
# beacon = esparlabctrl.beacon.Beacon()
    # assert True
    
    monkeypatch.setattr(net, "has_ssh", lambda ip : True)
    monkeypatch.setattr(SSHClient, "connect", lambda self, ip, username=None, password=None : None)
    monkeypatch.setattr(Beacon, "has_nrf_dongle", lambda self : True)
    monkeypatch.setattr(Beacon, "push_beacon_ctrl_app", lambda self : 0)
    monkeypatch.setattr(Beacon, "status", lambda self : BeaconState.IDLE)
    # monkeypatch.setattr(SSHClient, "exec_command", lambda self, cmd : (None, None, None))
    
    beacon = Beacon(TEST_BEACON_IP, TEST_BEACON_ID)