#!/usr/bin/env python3

from esparlabctrl.espar_lab.beacon import Beacon, BeaconConfig, BeaconState, init_beacons
from esparlabctrl.espar_lab.espar import Espar
from esparlabctrl.espar_lab.testcase import TestCase


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def generate_testcase_stationary_transmitter(
    beacons_count: int, tx_power: int = 0, jam_power: int = 4
) -> list[BeaconConfig]:
    for i in range(1, beacons_count+1):
        testcase_roles = [
            BeaconConfig(BeaconState.IDLE, 0) for _ in range(beacons_count)
        ]
        testcase_roles[0] = BeaconConfig(BeaconState.TX, tx_power)
        yield testcase_roles


def test_experiment_lab_characteristic(beacon_mock, network_mock, espar_mock):
    test_cycles = 10
    beacons: list[Beacon] = init_beacons(SUBNET, SERVER_IP)
    espar = Espar()

    for cycle in range(test_cycles):
        print(f"Test cycle {cycle+1}/{test_cycles}")
        for i, testcase_roles in enumerate(
            generate_testcase_stationary_transmitter(len(beacons))
        ):
            testcase = TestCase(
                espar,
                beacons,
                testcase_roles,
                name=f"Cycle: {cycle+1}; Test {i+1}",
            )
            testcase.run()
