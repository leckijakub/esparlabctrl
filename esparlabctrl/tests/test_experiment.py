from esparlabctrl.main import main

def test_experiment(beacon_mock, network_mock, espar_mock):
    main(["--config", "esparlabctrl/tests/data/experiment_config.json"])
