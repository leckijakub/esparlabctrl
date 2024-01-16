from .espar import ESPAR
from .beacon import Beacon, BeaconConfig, BeaconState
from .network import MAX_BEACONS

import concurrent.futures
import re


class Testcase:
    def __init__(
        self,
        espar: ESPAR,
        beacons: list[Beacon],
        roles: list[BeaconConfig],
        name="test",
        description="",
    ):
        self.espar = espar
        self.beacons = beacons
        self.roles = roles
        self.name = name
        self.description = description

    def config_beacons(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_BEACONS) as executor:
            results = list(
                executor.map(
                    lambda beacon, role: beacon.configure(role),
                    self.beacons,
                    self.roles,
                )
            )

    def idle_beacons(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_BEACONS) as executor:
            results = list(
                executor.map(
                    lambda beacon: beacon.configure(BeaconConfig(BeaconState.IDLE, 0)),
                    self.beacons,
                )
            )

    def run(self):
        print("Configuring beacons...")
        self.config_beacons()
        print("Starting espar...")
        with self.espar.run() as espar_proc:
            try:
                ok_count = 0
                for line in iter(espar_proc.stdout.readline, ""):
                    print(line, end="")
                    # use regex to get the float value from the line match '.* BPER: -XX.XX *'
                    if "BPER" in line:
                        bper = float(
                            re.search("BPER: \d+\.\d+", line).group().split(":")[1]
                        )
                        if bper <= 0.2:
                            ok_count += 1
                        else:
                            ok_count = 0
                        if ok_count >= 100:
                            print("Testcase passed.")
                            break

            except KeyboardInterrupt:
                print("KeyboardInterrupt caught. Exiting...")
        print("Espar finished.")
        self.idle_beacons()
