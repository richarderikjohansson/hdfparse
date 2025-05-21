import argparse
from .io import load_config, ParseInput


def main():
    config = load_config()
    help = config["help"]
    export = config["allowed_export"]

    parser = argparse.ArgumentParser(
        add_help=True,
        description="Command line tool to read HDF5 files from measurements and simulations",
    )

    parser.add_argument(dest="input", help=help["input"])
    parser.add_argument("--plot", help=help["plot"], action="store_true")
    parser.add_argument(
        "--export", help=help["export"], type=str, default=None
    )
    args = parser.parse_args()

    print(ParseInput(inp=args.input, export=args.export).resolve_path())
