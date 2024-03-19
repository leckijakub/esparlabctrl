from .espar import Espar
from .beacon import Beacon, BeaconConfig, BeaconState
from .network import MAX_BEACONS

import concurrent.futures
import re
import time


def default_final_condition(line: str) -> bool:
    if "BPER" in line:
        bper = float(re.search("BPER: \d+\.\d+", line).group().split(":")[1])
        if bper <= 0.2:
            default_final_condition.ok_counter += 1
        else:
            default_final_condition.ok_counter = 0
        if default_final_condition.ok_counter >= 100:
            return True
    return False
default_final_condition.ok_counter = 0

class TestCase:
    def __init__(
        self,
        espar: Espar,
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


    def run(self, final_condition=default_final_condition):
        print(f"Running testcase {self.name}...")
        print("Configuring beacons...")
        self.config_beacons()
        print("Starting espar...")
        start_time_ns = time.time_ns()
        with self.espar.run() as espar_proc:
            try:
                ok_count = 0
                for line in iter(espar_proc.stdout.readline, ""):
                    print(f"[{time.time_ns() - start_time_ns}]: {line}", end="")
                    if final_condition(line):
                        print("Testcase finished.")
                        break
            except KeyboardInterrupt:
                print("KeyboardInterrupt caught. Exiting...")
        print("Espar finished.")
        self.idle_beacons()

TestCase.__test__ = False