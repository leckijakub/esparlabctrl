from . import espar_lab

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
    def __init__(self, json: dict) -> None:
        self.config = json

    def run(self):
        print(f"Running experiment {self.config['name']}")
        print(f"Characteristics: {self.config['characteristics']}")
        print(f"TX Beacon: {self.config['tx_beacon']}")
        print(f"TX Power: {self.config['tx_power']}")
        print(f"Jammers: {self.config['jammers']}")
        print(f"Duration: {self.config['duration']}")

        espar = espar_lab.Espar()
        beacons = espar_lab.init_beacons()
