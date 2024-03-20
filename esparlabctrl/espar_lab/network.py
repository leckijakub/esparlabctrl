import nmap3

MAX_BEACONS = 48  # limitation of the ethernet switch


def get_network_devices(subnet) -> list[str]:
    nmd = nmap3.NmapHostDiscovery()
    nmap_result = nmd.nmap_no_portscan(subnet)

    # extract the list of hosts that are up
    hosts = []
    for host in nmap_result:
        if "state" not in nmap_result[host]:
            continue
        if "state" not in nmap_result[host]["state"]:
            continue
        if nmap_result[host]["state"]["state"] == "up":
            hosts.append(host)

    return hosts


# check if a host has ssh port open
def has_ssh(ip):
    nmap = nmap3.NmapScanTechniques()
    nmap_result = nmap.nmap_tcp_scan(ip, args="-p 22")[ip]

    if "ports" not in nmap_result:
        return False
    if len(nmap_result["ports"]) == 0:
        return False
    for port in nmap_result["ports"]:  # portid
        if "portid" not in port:
            continue
        if port["portid"] != "22":
            continue
        if "state" not in port:
            return False
        return port["state"] == "open"
    return False
