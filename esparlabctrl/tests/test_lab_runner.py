#!/usr/bin/env python3
import pytest
from esparlabctrl.espar_lab.beacon import BeaconConfig, BeaconState
from esparlabctrl.espar_lab.labrunner import LabRunner
from typing import Iterator


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def generate_testcase_stationary_transmitter(
    beacons_count: int, tx_power: int = 0, jam_power: int = 4
) -> 'Iterator[list[BeaconConfig]]':
    for i in range(1, beacons_count):
        testcase_roles = [
            BeaconConfig(BeaconState.IDLE, 0) for _ in range(beacons_count)
        ]
        testcase_roles[0] = BeaconConfig(BeaconState.TX, tx_power)
        testcase_roles[i] = BeaconConfig(BeaconState.JAM, jam_power)
        yield testcase_roles


def test_lab_runner_lab_characteristic():
    test_cycles = 3

    labRunner = LabRunner(SUBNET, SERVER_IP)
    for cycle in range(test_cycles):
        print(f"Test cycle {cycle+1}/{test_cycles}")
        for i, testcase_roles in enumerate(
            generate_testcase_stationary_transmitter(labRunner.num_beacons)
        ):
            print(f"Test case {i+1}/{labRunner.num_beacons - 1}")
            print("Configuring beacons...")
            labRunner.config_beacons(testcase_roles)
            print("Running lab...")
            labRunner.run()


@pytest.mark.mock
def test_lab_runner_lab_characteristic_mock(beacon_mock, network_mock, espar_mock):
    test_lab_runner_lab_characteristic()
