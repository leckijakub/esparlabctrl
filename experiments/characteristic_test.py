#!/usr/bin/env python3

from esparlabctrl.espar_lab.beacon import Beacon, BeaconConfig, BeaconState
from esparlabctrl.espar_lab.espar import Espar
from esparlabctrl.espar_lab.labrunner import LabRunner
from esparlabctrl.labctrl import init_beacons


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def generate_testcase_stationary_transmitter(
    beacons_count: int, tx_power: int = 0
) -> list[BeaconConfig]:
    for i in range(0, beacons_count):
        testcase_roles = [
            BeaconConfig(BeaconState.IDLE, 0) for _ in range(beacons_count)
        ]
        testcase_roles[i] = BeaconConfig(BeaconState.TX, tx_power)
        # testcase_roles[i] = BeaconConfig(BeaconState.JAM, jam_power)
        yield testcase_roles


def main():
    test_cycles = 1
    beacons: list[Beacon] = init_beacons(SUBNET, SERVER_IP)
    espar = Espar()

    for cycle in range(test_cycles):
        print(f"Test cycle {cycle+1}/{test_cycles}")
        # for i, testcase_roles in enumerate(generate_testcase_stationary_transmitter(2)):
        for i, testcase_roles in enumerate(
            generate_testcase_stationary_transmitter(len(beacons))
        ):
            testcase = LabRunner(
                espar,
                beacons,
                testcase_roles,
                name=f"Cycle: {cycle+1}; Test {i+1}",
            )
            testcase.run()


if __name__ == "__main__":
    main()
