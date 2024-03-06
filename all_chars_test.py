#!/usr/bin/env python3

from espar_lab.beacon import Beacon, BeaconConfig, BeaconState
from espar_lab.espar import ESPAR
from espar_lab.testcase import Testcase
from labctrl import init_beacons

import re


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def generate_testcase_stationary_transmitter(
    beacons_count: int, tx_power: int = 0, jam_power: int = 4
) -> list[BeaconConfig]:
    for i in range(1, beacons_count):
        testcase_roles = [
            BeaconConfig(BeaconState.IDLE, 0) for _ in range(beacons_count)
        ]
        testcase_roles[0] = BeaconConfig(BeaconState.TX, tx_power)
        testcase_roles[i] = BeaconConfig(BeaconState.JAM, jam_power)
        yield testcase_roles


def main():
    test_cycles = 100
    beacons: list[Beacon] = init_beacons(SUBNET, SERVER_IP)
    espar = ESPAR()

    for cycle in range(test_cycles):
        print(f"Test cycle {cycle+1}/{test_cycles}")
        # for i, testcase_roles in enumerate(generate_testcase_stationary_transmitter(2)):
        for i, testcase_roles in enumerate(
            generate_testcase_stationary_transmitter(len(beacons))
        ):
            testcase = Testcase(
                espar,
                beacons,
                testcase_roles,
                name=f"Cycle: {cycle+1}; Test {i+1}",
            )
            testcase.run(final_condition=lambda line: "CHAR" in line and re.search("CHAR: [01]+", line).group().split(" ")[1] == "111111111111")


if __name__ == "__main__":
    main()
