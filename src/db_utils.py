from sqlalchemy import create_engine

# kvazi module private vars
__db_cfg = None
__db_conn = None


class DbConfig(dict):
    # hm... kvoli IDE aby rozpoznalo typy
    DB_HOST = None
    DB_USER = None
    DB_PASSWORD = None
    DB_DATABASE = None
    DB_PORT = None

    # "Bunch" pattern magic
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def set_db_config(cfg: dict) -> DbConfig:
    global __db_cfg  # hm... smells... ale neviem ako inak
    __db_cfg = DbConfig(cfg)
    return __db_cfg


def get_db_config() -> DbConfig:
    global __db_cfg
    return __db_cfg


def get_db_conn(debug=False):
    global __db_conn

    if __db_conn is None:
        db_cfg = get_db_config()
        conn_str = (
            f"postgresql://{db_cfg.DB_USER}:{db_cfg.DB_PASSWORD}"
            f"@{db_cfg.DB_HOST}:{db_cfg.DB_PORT}/{db_cfg.DB_DATABASE}"
        )
        __db_conn = create_engine(conn_str)

    __db_conn.echo = debug

    return __db_conn


def db_execute(sql: str, debug=False):
    conn = get_db_conn(debug)
    return conn.execute(sql)
