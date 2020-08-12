"""Main application entry"""

import os
import re
import sys

from dotenv import load_dotenv

from .db_utils import db_execute, get_db_config, set_db_config
from .schema_utils import get_schema
from .args_utils import create_arg_parser


def create_logger(is_silent):
    def _logger(*args):
        if not is_silent:
            print(*args)

    return _logger


def main():
    try:
        _args = create_arg_parser().parse_args()
        _logger = create_logger(_args.silent)

        # laod .env... @see parse_cli
        load_dotenv(_args.env)

        # collect db config envs (and save it for later)
        # fmt: off
        db_cfg = set_db_config({ key: os.getenv(key) for key in [
            "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_DATABASE", "DB_PORT"
        ]})
        # fmt: on
        # print(db_cfg)

        # warn pm production
        is_production = os.getenv("PYTHON_ENV", "production") == "production"
        if is_production and not _args.force and not _args.dry:
            _logger(
                "This is not intended to be run in production unless --force is used"
            )
            sys.exit(0)

        # are you sure?
        if not _args.yes and not _args.dry:
            yn = input(
                f"\nThis will recreate sql schema in "
                f"postgres://{db_cfg.DB_HOST}:{db_cfg.DB_PORT}/{db_cfg.DB_DATABASE} ..."
                "\nAre you sure? [y/n]\n"
            ).strip()
            if not re.match(re.compile("^y(es)?$", re.IGNORECASE), yn):
                _logger("Aborted")
                sys.exit(0)

        # collect schema
        try:
            sql = ""
            for indir in _args.indir:
                sql += get_schema(indir, os.getenv("TBLPREFIX", ""))
        except FileNotFoundError as e:
            print(str(e))
            sys.exit(2)

        if _args.dry:
            print(sql)
            sys.exit(0)

        # finally execute
        try:
            res = db_execute(sql, debug=False)
        except Exception as e:
            print("SQL exec error: " + str(e))
            sys.exit(2)

        _logger("OK, done")
        sys.exit(0)

    except KeyboardInterrupt:
        sys.exit(0)
