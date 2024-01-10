import nmap3
import paramiko
from pprint import pprint

def get_network_devices(subnet):
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
    for port in nmap_result["ports"]:    #portid
        if "portid" not in port:
            continue
        if port["portid"] != "22":
            continue
        if "state" not in port:
            return False
        return port["state"] == "open"
    return False


# check if a host has a USB device with the given vendor and product id
def has_nrf_dongle(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="root", password="",)
    # 1915:520f is the vendor:product id for the nRF52840 dongle
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("lsusb | grep 1915:520f")
    return ssh_stdout.channel.recv_exit_status() == 0


def is_beacon(ip):
    return has_ssh(ip) and has_nrf_dongle(ip)
