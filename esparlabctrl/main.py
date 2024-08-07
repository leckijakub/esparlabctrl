import argparse
import json
import jsonschema
from .espar_lab import LabRunner
from .experiment import Experiment
from .cli import Cli

schema = {
    "type": "object",
    "properties": {
        "experiments": {"type": "array", "items": Experiment.json_schema},
        "lab": {
            "type": "object",
            "properties": {
                "server_ip": {"type": "string"},
                "subnet": {"type": "string"},
            },
            "required": ["server_ip", "subnet"],
        },
    },
    "required": ["experiments"],
}


def parse_args(sysargs):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config file")
    parser.add_argument("--server_ip", help="server ip", default="192.0.2.0")
    parser.add_argument("--subnet", help="subnet", default="192.0.2.0/24")
    return parser.parse_args(sysargs)


def main(sysargs):
    args = parse_args(sysargs)
    if args.config is None:
        cli = Cli(args.subnet, args.server_ip)
        cli.run()
        exit(0)

    print(f"config file: {args.config}")
    with open(args.config, "r") as f:
        json_obj = json.load(f)

    try:
        jsonschema.validate(json_obj, schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Config loading error: {e.message}")
        exit(1)

    labRunner = LabRunner(json_obj["lab"]["subnet"], json_obj["lab"]["server_ip"])

    for experiment in json_obj["experiments"]:
        exp = Experiment(experiment, labRunner)
        exp.run()
