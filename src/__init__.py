import os
import re
import sys

from dotenv import load_dotenv

from .args_utils import parse_cli
from .file_utils import read_files

# kvazi constants... hm...
DB_HOST = "DB_HOST"
DB_USER = "DB_USER"
DB_PASSWORD = "DB_PASSWORD"
DB_DATABASE = "DB_DATABASE"
DB_PORT = "DB_PORT"


def create_logger(is_silent):
    def _logger(*args):
        if not is_silent:
            print(*args)

    return _logger


def main():
    try:
        _args = parse_cli()
        _logger = create_logger(_args.silent)

        # laod .env... @see parse_cli
        load_dotenv(_args.env)

        # collect db config envs
        db_cfg = {key: os.getenv(key) for key in [
            DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT
        ]}

        is_production = os.getenv("PYTHON_ENV", "production") == "production"
        if is_production and not _args.force:
            _logger(
                "This is not intended to be run in production unless --force is used"
            )
            sys.exit(0)

        # maybe exit...
        if not _args.yes:
            yn = input(
                f"\nThis will recreate sql schema in "
                f"postgres://{db_cfg[DB_HOST]}:{db_cfg[DB_PORT]}/{db_cfg[DB_DATABASE]} ..."
                "\nAre you sure? [y/n]\n"
            ).strip()
            if not re.match(re.compile("^y(es)?$", re.IGNORECASE), yn):
                _logger("Bye, nothing to do...")
                sys.exit(0)

        # read what we have
        files = read_files(_args.indir)
        # _logger(files)

    except KeyboardInterrupt:
        sys.exit(0)

