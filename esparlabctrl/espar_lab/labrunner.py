from .espar import Espar
from .beacon import Beacon, BeaconConfig, BeaconState, init_beacons
from .network import MAX_BEACONS

import concurrent.futures
import re
import time
import sys


def default_final_condition(line: str) -> bool:
    if "BPER" in line:
        bper = float(re.search(r"BPER: \d+\.\d+", line).group().split(":")[1])
        if bper <= 0.2:
            default_final_condition.ok_counter += 1
        else:
            default_final_condition.ok_counter = 0
        if default_final_condition.ok_counter >= 100:
            return True
    return False
default_final_condition.ok_counter = 0

class LabRunner:
    def __init__(
        self,
        subnet: str,
        server_ip: str
    ):
        self.espar = Espar()
        self.beacons = init_beacons(subnet, server_ip)
        # self.roles = [BeaconConfig(BeaconState.IDLE, 0) for _ in range(len(self.beacons))]

    @property
    def num_beacons(self):
        return len(self.beacons)

    def config_beacons(self, roles: 'list[BeaconConfig]'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_BEACONS) as executor:
            results = list(
                executor.map(
                    lambda beacon, role: beacon.configure(role),
                    self.beacons,
                    roles,
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

    def config_espar_char(self, characteristic: int):
        self.espar.set_char(characteristic)

    def run(self, final_condition=default_final_condition, output=None, timestamp=True):

        default_final_condition.ok_counter = 0
        print("Starting espar...")
        start_time_ns = time.time_ns()
        if output:
            f = open(output, 'w')
        else:
            f = sys.stdout
        with self.espar.run() as espar_proc:
            try:
                ok_count = 0
                for line in iter(espar_proc.stdout.readline, ""):
                    if timestamp:
                        print(f"[{time.time_ns() - start_time_ns}]: {line}", end="", file=f)
                    else:
                        print(line, end="", file=f)
                    if final_condition(line):
                        print("Testcase finished.")
                        break
            except KeyboardInterrupt:
                print("KeyboardInterrupt caught. Exiting...")
        print("Espar finished.")
        self.idle_beacons()

LabRunner.__test__ = False
