import paramiko
import enum
import subprocess

from . import network as net


class BeaconState(enum.IntEnum):
    JAM = 0
    TX = 1
    RX = 2
    IDLE = 3


class BeaconConfig:
    def __init__(self, state: BeaconState, power: int):
        self.state = state
        self.power = power


class Beacon:
    def __init__(self, ip, id, username="root", password=""):
        self.ip = ip
        self.id = id
        self.username = username
        self.password = password
        self.beacon_ctrl_app = "/tmp/beacon_ctrl"  # TODO: change this to the correct path after updating the beacon_ctrl app in the system build
        self.beacon_dev_str = "/dev/ttyACM0"

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

        if self.push_beacon_ctrl_app() != 0:
            raise Exception(f"Couldn't push beacon_ctrl app to beacon {self.ip}")

        if self.status() == None:
            raise Exception(f"Couldn't get status of beacon {self.ip}")

    # check if a host has a USB device with the given vendor and product id
    def has_nrf_dongle(self):
        # 1915:520f is the vendor:product id for the nRF52840 dongle
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
            "lsusb | grep 1915:520f"
        )
        return ssh_stdout.channel.recv_exit_status() == 0

    def status(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
            f"{self.beacon_ctrl_app} {self.beacon_dev_str} status | grep 'DUT state'"
        )
        if ssh_stdout.channel.recv_exit_status() != 0:
            raise Exception(f"Error getting beacon status: {ssh_stderr.read()}")
        output_lines = ssh_stdout.readlines()
        for line in output_lines:
            if "DUT state" in line:
                state = int(
                    line.split(":")[1].strip()
                )  # split the line on the colon and take the second part
                if state in iter(
                    BeaconState
                ):  # check if the state is a valid BeaconState
                    return BeaconState(state)
        return None

    def push_beacon_ctrl_app(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
            f"ls {self.beacon_ctrl_app}"
        )
        if ssh_stdout.channel.recv_exit_status() == 0:
            # beacon_ctrl app already exists, don't push it
            return 0

        # beacon_ctrl app not found, push it
        proc = subprocess.Popen(
            ["scp", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=accept-new", "scripts/beacon_ctrl", f"root@{self.ip}:{self.beacon_ctrl_app}"]
        )
        proc.wait()
        return proc.returncode
        # ftp_client = self.ssh.open_sftp()
        # ftp_client.put("scripts/beacon_ctrl", self.beacon_ctrl_app)
        # print(f"Beacon {self.id} beacon_ctrl app pushed.")
        # ftp_client.close()

    def configure(self, config: BeaconConfig):
        if config.state == BeaconState.IDLE:
            action = "idle"
        elif config.state == BeaconState.RX:
            raise Exception("RX not supported yet.")
        elif config.state == BeaconState.TX:
            action = "tx"
        elif config.state == BeaconState.JAM:
            action = "jam"

        if config.state == BeaconState.IDLE:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
                f"{self.beacon_ctrl_app} {self.beacon_dev_str} {action}"
            )
        else:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
                f"{self.beacon_ctrl_app} {self.beacon_dev_str} {action} {config.power}"
            )
        if ssh_stdout.channel.recv_exit_status() != 0:
            raise Exception(f"Error setting beacon state: {ssh_stderr.read()}")
        else:
            print(f"Beacon {self.id} configured as {action} with power {config.power}.")
