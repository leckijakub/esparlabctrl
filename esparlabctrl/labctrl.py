#!/usr/bin/env python3

# For unknown reasons the concorrent executor.submit method is causing terminal to not echo input after program finishes.
# as a workaround, run `stty sane` after program finishes.
from .espar_lab.beacon import Beacon, BeaconConfig, BeaconState, init_beacons
from .espar_lab.espar import Espar
from .espar_lab.labrunner import LabRunner


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def main():
    beacons: list[Beacon] = init_beacons(SUBNET, SERVER_IP)

    espar = Espar()

    testcase_1_roles = [BeaconConfig(BeaconState.IDLE, 0) for _ in beacons]
    testcase_1_roles[0] = BeaconConfig(BeaconState.TX, 0)
    testcase_1_roles[9] = BeaconConfig(BeaconState.JAM, 4)

    testcase_1 = LabRunner(
        espar,
        beacons,
        testcase_1_roles,
        name="Test 1",
    )
    testcase_1.run()


if __name__ == "__main__":
    main()
