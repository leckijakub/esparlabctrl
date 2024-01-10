import paramiko

from . import network as net


class Beacon:
    def __init__(self, ip, id, username="root", password=""):
        self.ip = ip
        self.id = id
        self.username = username
        self.password = password
        self.beacon_ctrl_app = "/tmp/beacon_ctrl"  # TODO: change this to the correct path after updating the beacon_ctrl app in the system build

        if not net.has_ssh(self.ip):
            raise Exception(f"Beacon {self.ip} does not have SSH enabled.")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.ip,
            username=self.username,
            password=self.password,
        )
        if not self.has_nrf_dongle():
            raise Exception(
                f"Beacon {self.ip} does not have an nRF52840 dongle attached."
            )

    # check if a host has a USB device with the given vendor and product id
    def has_nrf_dongle(self):
        # 1915:520f is the vendor:product id for the nRF52840 dongle
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("lsusb | grep 1915:520f")
        return ssh_stdout.channel.recv_exit_status() == 0

    def status(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
            f"{self.beacon_ctrl_app} /dev/ttyACM0 status | grep 'DUT state'"
        )
        if ssh_stdout.channel.recv_exit_status() != 0:
            raise Exception(f"Error getting beacon status: {ssh_stderr.read()}")
        return ssh_stdout.readlines()[0]
