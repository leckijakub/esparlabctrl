import subprocess
from contextlib import contextmanager
import pylink
import sys
import re
import statistics

import time
def rtt_read_until(jlink, expected):
    output = ""
    while True:
        bytes = jlink.rtt_read(0, 1024)
        if bytes:
            read_str = "".join(map(chr, bytes))
            output += read_str
            # sys.stdout.write(read_str)
            # sys.stdout.flush()
            if expected in read_str:
                break
        time.sleep(0.1)
    return output

def rtt_write(jlink, cmd):
    bytes = list(bytearray(cmd, "utf-8") + b"\x0A\x00")
    # print(f"CMD length: {len(bytes)}")
    bytes_written = 0
    while bytes_written < len(bytes):
        bytes_written += jlink.rtt_write(0, bytes[bytes_written:])
        # print(f"Written {bytes_written} bytes: {cmd}")

class Espar:
    def __init__(self):
        self.dev_str = "/dev/ttyUSB0"
        self.jlink = pylink.JLink()
        print("connecting to JLink...")
        self.jlink.open()
        print("connecting to nRF52840_xxAA...")
        self.jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        self.jlink.connect("nRF52840_xxAA")
        print("connected, starting RTT...")
        self.jlink.rtt_start()
        print("Waiting for prompt...")
        # cmd = list(bytearray("", "utf-8") + b"\x0A\x00")
        # self.jlink.rtt_write(0, cmd)
        rtt_write(self.jlink, "")
        while True:
            bytes = self.jlink.rtt_read(0, 1024)
            if bytes:
                output = "".join(map(chr, bytes))
                if "espar_cli" in output:
                    break
            time.sleep(0.1)
            rtt_write(self.jlink, "")
            # self.jlink.rtt_write(0, cmd)
        print("Prompt received")


    def set_char(self, char):
        raise NotImplementedError

    def test_char(self, char):
        bper_arr = []
        rssi_arr = []

        rtt_write(self.jlink, f"rx sct {char} 10\n")
        try:
            data = rtt_read_until(self.jlink, "SCT stopped")
            for line in data.split("\n"):
                    m = re.search(r"[BATCH [0-9]+ SUMMARY]: ESPAR CHAR: (\d+), BPER: (\d+\.\d+), RSSI: (-?\d+\.\d+)", line)
                    if m:
                        char, bper, rssi = m.groups()
                        bper_arr.append(float(bper))
                        rssi_arr.append(float(rssi))
        finally:
            pass
            # rtt_write(self.jlink, "idle\n")
            # rtt_read_until(self.jlink, "espar_cli")
        return statistics.mean(bper_arr), statistics.mean(rssi_arr)

    def reset(self):
        # nrfjprog --family NRF52 --reset
        reset_cmd = subprocess.Popen(
            ["nrfjprog", "--family", "NRF52", "--reset"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        reset_cmd.wait()
        if reset_cmd.returncode != 0:
            raise Exception(f"Error resetting device: {reset_cmd.stderr.read()}")

    def halt(self):
        # nrfjprog --family NRF52 --halt
        tries = 3
        while tries:
            halt_cmd = subprocess.Popen(
                ["nrfjprog", "--family", "NRF52", "--halt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            halt_cmd.wait()
            if halt_cmd.returncode == 0:
                return
            time.sleep(5)
            tries -= 1
        raise Exception(f"Error halting device: {halt_cmd.stderr.read()}")

    @contextmanager
    def run(self) -> subprocess.Popen:
        self.reset()
        popen = subprocess.Popen(
            ["pylink-rtt", "nRF52840_xxAA"],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        yield popen
        popen.stdout.close()
        popen.kill()
        self.halt()
