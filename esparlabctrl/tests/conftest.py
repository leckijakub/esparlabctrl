import pytest
import subprocess
from unittest.mock import MagicMock
from esparlabctrl.espar_lab import BeaconState, BeaconConfig

def pytest_addoption(parser):
    parser.addoption(
        "--mock",
        action="store_true",
        default=False,
        help="Run mock tests",
    )

def pytest_collection_modifyitems(config, items):
    if not config.getoption("--mock"):
        skipper = pytest.mark.skip(reason="Only run when --mock is given")
        for item in items:
            if "mock" in item.keywords:
                item.add_marker(skipper)
    else:
        skipper = pytest.mark.skip(reason="Don't run on real hardware when --mock is given")
        for item in items:
            if "mock" not in item.keywords:
                item.add_marker(skipper)


mock_beacon_config = BeaconConfig(BeaconState.IDLE, 0)

def mock_beacon_configure(self, config):
    global mock_beacon_config
    mock_beacon_config = config
    print(f"Beacon {self.id} configured as {config.state} with power {config.power}.")


@pytest.fixture
def data_dir(request):
    return f'{request.fspath.dirname}/data'


@pytest.fixture(name="beacon_mock")
def fixture_beacon_mock(monkeypatch):
    monkeypatch.setattr("esparlabctrl.espar_lab.beacon.Beacon.has_nrf_dongle", lambda self: True)
    monkeypatch.setattr("esparlabctrl.espar_lab.beacon.Beacon.push_beacon_ctrl_app", lambda self: 0)
    monkeypatch.setattr("esparlabctrl.espar_lab.beacon.Beacon.status", lambda self: mock_beacon_config.state)
    monkeypatch.setattr("esparlabctrl.espar_lab.beacon.Beacon.configure", mock_beacon_configure)
    monkeypatch.setattr("esparlabctrl.espar_lab.beacon.paramiko.SSHClient.connect", lambda self, ip, username=None, password=None: None)
    yield
    monkeypatch.undo()


@pytest.fixture(name="network_mock")
def fixture_network_mock(monkeypatch):
    monkeypatch.setattr("esparlabctrl.espar_lab.network.has_ssh", lambda ip: True)
    monkeypatch.setattr("esparlabctrl.espar_lab.network.get_network_devices", lambda subnet: ["192.168.0.1", "192.168.0.2"])
    yield
    monkeypatch.undo()


@pytest.fixture(name="espar_mock")
def fixture_espar_mock(monkeypatch, data_dir):
    def mock_popen(*args, **kwargs):
        mock = MagicMock()
        with open(f'{data_dir}/test_espar_output.txt', 'r') as f:
            mock.stdout.readline.side_effect = f.readlines()
        return mock
    monkeypatch.setattr("esparlabctrl.espar_lab.espar.Espar.reset", lambda self: None)
    monkeypatch.setattr("esparlabctrl.espar_lab.espar.Espar.halt", lambda self: None)
    monkeypatch.setattr("esparlabctrl.espar_lab.espar.Espar.set_char", lambda self, char: None)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    yield
    monkeypatch.undo()
