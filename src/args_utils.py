import argparse
import os
import sys
from os.path import abspath, dirname, join, abspath


def parse_cli():
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--indir", required=True, help="Source directory containing sql files"
        )

        # support for optional path, fallback to sane default
        default_env = join(os.getcwd(), ".env")
        parser.add_argument(
            "--env",
            help="Optional path to .env file (default: " + default_env + ")",
            default=default_env,
        )

        parser.add_argument(
            "--force",
            action="store_true",
            help="Will run even on production env (via PYTHON_ENV)",
        )

        parser.add_argument(
            "--yes",
            action="store_true",
            help='Do not ask for confirmation and assume "yes"',
        )

        parser.add_argument(
            "--silent", action="store_true", help="Do not produce stdout output"
        )

        return parser.parse_args()
    except argparse.ArgumentError as err:
        print(str(err))
        sys.exit(2)
