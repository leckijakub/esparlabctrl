import pytest
from esparlabctrl.main import main

def test_experiment():
    main(["--config", "esparlabctrl/tests/data/experiment_config.json"])


@pytest.mark.mock
def test_experiment_mock(beacon_mock, network_mock, espar_mock):
    test_experiment()
