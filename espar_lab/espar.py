import subprocess
from contextlib import contextmanager

import time


class ESPAR:
    def __init__(self):
        self.dev_str = "/dev/ttyUSB0"

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
