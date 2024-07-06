import inquirer.themes
from .espar_lab import LabRunner
from .espar_lab.beacon import BeaconConfig, BeaconState
import inquirer
import re
from inquirer.themes import GreenPassion

THEME = GreenPassion()


class Cli:

    def __init__(self, subnet, server_ip):
        self.labRunner = LabRunner(subnet, server_ip)

    def run(self):
        questions = [
            inquirer.List(
                "action",
                message="Actions",
                choices=[
                    "Configure beacons",
                    # "Set characteristic",
                    "Run experiment",
                    "Exit",
                ],
            )
        ]
        while True:
            answers = inquirer.prompt(questions, theme=THEME)
            if answers["action"] == "Configure beacons":
                self.beacon_config()
            elif answers["action"] == "Run experiment":
                self.labRunner.run()
            elif answers["action"] == "Exit":
                break

    def beacon_config(self):
#         roles = []
#         for i in range(self.labRunner.num_beacons):
#             state_question = inquirer.List(
#                 "state",
#                 message=f"Beacon {i} role",
#                 choices=["IDLE", "TX", "JAM"],
#             )
#             state = inquirer.prompt([state_question], theme=THEME)["state"]
#             if state == "IDLE":
#                 roles.append(BeaconConfig(BeaconState.IDLE, 0))
#             else:
#                 power_question = inquirer.Text(
#                     "power",
#                     message=f"Beacon {i} power level (dBm) (default 0)",
#                     validate=lambda _, x: re.match("-?\d?", x),
#                 )
#                 power = inquirer.prompt([power_question], theme=THEME)["power"]
#                 if power == "":
#                     power = 0
#                 power = int(power)
#                 roles.append(BeaconConfig(BeaconState[state], power))
#             print(roles[i].state, roles[i].power)
#         self.labRunner.config_beacons(roles)
        def get_beacon_config_choices():
            beacon_config_choices = []
            for i in range(self.labRunner.num_beacons):
                beacon_state = self.labRunner.beacons[i].status()
                prefix = beacon_state.name
                # for now beacons don't report their power in status command
                # if beacon_state in (BeaconState.TX, BeaconState.JAM):
                #     prefix += f" {self.labRunner.beacons[i].power}"
                beacon_config_choices.append(f"[{prefix}] Beacon " + str(i))
            beacon_config_choices.append("Exit")
            return beacon_config_choices

        while True:
            beacon_config_choices = get_beacon_config_choices()
            beacon_config_questions = [inquirer.List("beacon", message="Beacon to configure", choices=beacon_config_choices)]
            beacon_config_answers = inquirer.prompt(beacon_config_questions, theme=THEME)
            if beacon_config_answers["beacon"] == "Exit":
                break
            else:
                beacon = int(beacon_config_answers["beacon"].split(" ")[-1])
                state_question = inquirer.List("state", message="Select new beacon role", choices=["IDLE", "TX", "JAM"])
                state = inquirer.prompt([state_question], theme=THEME)["state"]
                if state == "IDLE":
                    role = BeaconConfig(BeaconState.IDLE, 0)
                else:
                    power_question = inquirer.Text("power", message="Power level (dBm) (default 0)", validate=lambda _, x: re.match("-?\d?", x))
                    power = inquirer.prompt([power_question], theme=THEME)["power"]
                    if power == "":
                        power = 0
                    power = int(power)
                    role = BeaconConfig(BeaconState[state], power)
                self.labRunner.beacons[beacon].configure(role)

def cli(args):
    labRunner = LabRunner(args.subnet, args.server_ip)
    questions = [
        inquirer.List(
            "action",
            message="Actions",
            choices=[
                "Configure beacons",
                "Set characteristic",
                "Run experiment",
                "Exit",
            ],
        )
    ]
    while True:
        answers = inquirer.prompt(questions, theme=THEME)
        if answers["action"] == "Configure beacons":
            roles = []
            for i in range(labRunner.num_beacons):
                state_question = inquirer.List(
                    "state",
                    message=f"Beacon {i} role",
                    choices=["IDLE", "TX", "JAM"],
                )
                state = inquirer.prompt([state_question], theme=THEME)["state"]
                if state == "IDLE":
                    roles.append(BeaconConfig(BeaconState.IDLE, 0))
                else:
                    power_question = inquirer.Text(
                        "power",
                        message=f"Beacon {i} power level (dBm) (default 0)",
                        validate=lambda _, x: re.match("-?\d?", x),
                    )
                    power = inquirer.prompt([power_question], theme=THEME)["power"]
                    if power == "":
                        power = 0
                    power = int(power)
                    roles.append(BeaconConfig(BeaconState[state], power))
                print(roles[i].state, roles[i].power)
            labRunner.config_beacons(roles)
        # elif answers["action"] == "Set characteristic":
        #     characteristic = inquirer.text(message="Characteristic")
        #     labRunner.config_espar_char(int(characteristic))
        elif answers["action"] == "Run experiment":
            labRunner.run()
        elif answers["action"] == "Exit":
            break
