from .espar_lab import LabRunner, BeaconConfig, BeaconState

import time


class Experiment():
    json_schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "characteristics": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    },
                    "tx_beacon": {"type": "integer"},
                    "tx_power": {"type": "integer"},
                    "jammers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "power": {"type": "integer"}
                            },
                            "required": ["id", "power"]
                        }
                    },
                    "duration": {"type": "integer"}
                },
                "required": ["name", "characteristics", "tx_beacon", "tx_power", "jammers", "duration"]
            }
    def __init__(self, json: dict, labRunner: LabRunner) -> None:
        self.config = json
        self.labRunner = labRunner
        self.start_time = time.gmtime(0)

    def final_condition_duration(self, line):
        # Set start time if it is not set
        if self.start_time == time.gmtime(0):
            self.start_time = time.time()
        return time.time() - self.start_time >= self.config['duration']

    def run(self):
        print(f"Running experiment {self.config['name']}")
        print(f"Characteristics: {self.config['characteristics']}")
        print(f"TX Beacon: {self.config['tx_beacon']}")
        print(f"TX Power: {self.config['tx_power']}")
        print(f"Jammers: {self.config['jammers']}")
        print(f"Duration: {self.config['duration']}")

        roles = [BeaconConfig(BeaconState.IDLE, 0) for _ in range(self.labRunner.num_beacons)]
        roles[self.config['tx_beacon']] = BeaconConfig(BeaconState.TX, self.config['tx_power'])
        for jammer in self.config['jammers']:
            roles[jammer['id']] = BeaconConfig(BeaconState.JAM, jammer['power'])

        self.labRunner.config_beacons(roles)
        #for i in range(1, len(self.config['characteristics'])):
        #    print(f"Configuring characteristic {i}")
        #    self.labRunner.config_espar_char(self.config['characteristics'][i])
        print("Running lab...")
        self.labRunner.run(final_condition=self.final_condition_duration)
