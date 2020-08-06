import os
import re
import sys

from dotenv import load_dotenv

from .args_utils import parse_cli
from .file_utils import read_files


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

        # kvazi "consts" hm...
        DB_HOST = "DB_HOST"
        DB_USER = "DB_USER"
        DB_PASSWORD = "DB_PASSWORD"
        DB_DATABASE = "DB_DATABASE"
        DB_PORT = "DB_PORT"

        # collect db config envs
        db_cfg_keys = [DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT]
        db_cfg = {key: os.getenv(key) for key in db_cfg_keys}
        # _logger(db_cfg)

        is_production = os.getenv("PYTHON_ENV", "production") == "production"
        if is_production and not _args.force:
            _logger(
                "This is not intended to be run in production unless --force is used"
            )
            sys.exit(0)

        # maybe do not continue...
        if not _args.yes:
            yn = input(
                f"\nThis will recreate sql schema in "
                f"postgres://{db_cfg[DB_HOST]}:{db_cfg[DB_PORT]}/{db_cfg[DB_DATABASE]} ..."
                "\nAre you sure? [y/n]\n"
            ).strip()
            if not re.match(re.compile("^y(es)?$", re.IGNORECASE), yn):
                _logger("Bye, nothing to do...")
                return

    except KeyboardInterrupt:
        sys.exit(0)

    # files = read_files(args.indir)
