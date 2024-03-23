import argparse
import json
import jsonschema
from python_json_config import ConfigBuilder
from .experiment import Experiment

schema= {
    "type": "object",
    "properties": {
        "experiments": {
            "type": "array",
            "items": Experiment.json_schema
        },
        "lab": {
            "type": "object",
            "properties": {
                "server_ip": {"type": "string"},
                "subnet": {"type": "string"}
            },
            "required": ["server_ip", "subnet"]
        }
    },
    "required": ["experiments"]
}


parser = argparse.ArgumentParser()
parser.add_argument("--config", help="path to config file")
args = parser.parse_args()
print(f"config file: {args.config}")
with open(args.config, "r") as f:
    json_obj = json.load(f)

try:
    jsonschema.validate(json_obj, schema)
except jsonschema.exceptions.ValidationError as e:
    print(f"Config loading error: {e.message}")
    exit(1)

for experiment in json_obj["experiments"]:
    exp = Experiment(experiment)
    exp.run()
