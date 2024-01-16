#!/usr/bin/env python3

# For unknown reasons the concorrent executor.submit method is causing terminal to not echo input after program finishes.
# as a workaround, run `stty sane` after program finishes.

import concurrent.futures

from espar_lab import network
from espar_lab.beacon import Beacon, BeaconConfig, BeaconState
from espar_lab.espar import ESPAR
from espar_lab.testcase import Testcase


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"


def init_beacon(ip, id):
    try:
        beacon = Beacon(ip, id)
        return beacon
    except Exception as e:
        print(e)
        return None


def init_beacons(subnet, server_ip):
    hosts = network.get_network_devices(subnet)
    beacons_addrs = [host for host in hosts if host != server_ip]
    beacons = []
    beacon_cnt = 0
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=network.MAX_BEACONS
    ) as executor:
        futures = {}
        for beacon_addr in beacons_addrs:
            futures[executor.submit(init_beacon, beacon_addr, beacon_cnt)] = beacon_addr
            beacon_cnt += 1
        for future in concurrent.futures.as_completed(futures):
            beacon_addr = futures[future]
            beacon = future.result()
            if beacon is not None:
                beacons.append(beacon)
                print(f"Beacon {beacon.id} with IP: {beacon.ip} created.")
            else:
                print(f"Failed to create beacon with IP: {beacon_addr}.")
    beacons.sort(key=lambda beacon: beacon.id)
    return beacons


def main():
    beacons: list[Beacon] = init_beacons(SUBNET, SERVER_IP)

    espar = ESPAR()

    testcase_1_roles = [BeaconConfig(BeaconState.IDLE, 0) for _ in beacons]
    testcase_1_roles[0] = BeaconConfig(BeaconState.TX, 0)
    testcase_1_roles[9] = BeaconConfig(BeaconState.JAM, 4)

    testcase_1 = Testcase(
        espar,
        beacons,
        testcase_1_roles,
        name="Test 1",
    )
    testcase_1.run()


if __name__ == "__main__":
    main()
