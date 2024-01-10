#!/usr/bin/env python3

from pprint import pprint

from espar_lab import network
from espar_lab.beacon import Beacon


SERVER_IP = "192.0.2.0"
SUBNET = "192.0.2.0/24"

def main():
    hosts = network.get_network_devices(SUBNET)
    beacons_addrs = [host for host in hosts if host != SERVER_IP]
    pprint(beacons_addrs)

    beacons: list[Beacon] = []
    beacon_cnt = 0
    for beacon_addr in beacons_addrs:
        print(f"Checking {beacon_addr}...",end="")
        if not network.is_beacon(beacon_addr):
            print("FAIL")
        else:
            print("OK")
            beacons.append(Beacon(beacon_addr, beacon_cnt))
            beacon_cnt += 1

    print(f"Found {len(beacons)} beacons.")




if __name__ == "__main__":
    main()
