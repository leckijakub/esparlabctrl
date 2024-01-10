#!/usr/bin/env python3

# For unknown reasons the concorrent executor.submit method is causing terminal to not echo input after program finishes.
# as a workaround, run `stty sane` after program finishes.

from pprint import pprint
import concurrent.futures

from espar_lab import network
from espar_lab.beacon import Beacon


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"

def init_beacon(ip, id):
    try:
        beacon = Beacon(ip, id)
        return beacon
    except Exception as e:
        print(e)
        return None

def main():
    hosts = network.get_network_devices(SUBNET)
    beacons_addrs = [host for host in hosts if host != SERVER_IP]
    beacons: list[Beacon] = []
    beacon_cnt = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for beacon_addr in beacons_addrs:
            futures[executor.submit(init_beacon, beacon_addr, beacon_cnt)] = beacon_addr
            beacon_cnt += 1
        beacon_cnt = 0
        for future in concurrent.futures.as_completed(futures):
            beacon_addr = futures[future]
            beacon = future.result()
            if beacon is not None:
                beacons.append(beacon)
                print(f"Beacon {beacon.id} with IP: {beacon.ip} created.")
            else:
                print(f"Failed to create beacon with IP: {beacon_addr}.")


#    print("Checking beacon status...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda beacon: beacon.status(), beacons))

    for result, beacon in zip(results, beacons):
        print(f"Beacon {beacon.id} ({beacon.ip}) status: {result}")



if __name__ == "__main__":
    main()
