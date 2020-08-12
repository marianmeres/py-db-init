import argparse
import os
from os.path import join


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Utility to collect and execute sql files from a given directory. "
            "Execution of files is sorted based on their declared dependency "
            "via magic sql comment: -- ## require <filename>"
        )
    )

    parser.add_argument(
        "--indir",
        action="append",
        required=True,
        help="Source directory containing sql files. Multiple --indir args are allowed.",
    )

    # support for optional path, fallback to sane default
    default_env = join(os.getcwd(), ".env")
    parser.add_argument(
        "--env",
        help=f"Optional path to .env file (default: {default_env})",
        default=default_env,
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Will run even on production env (detected via PYTHON_ENV)",
    )

    parser.add_argument(
        "--yes",
        action="store_true",
        help='Do not ask for confirmation and assume "yes"',
    )

    parser.add_argument(
        "--silent", action="store_true", help="Do not produce stdout output"
    )

    parser.add_argument(
        "--dry",
        action="store_true",
        help="Just return collected sql, but do not execute it against db",
    )

    return parser
