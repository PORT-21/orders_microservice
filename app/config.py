import logging
import os

from lib.env_helpers import get_bool_from_env, get_list_from_env
from lib.env_helpers import get_int_from_env

# region main config
DJANGO_MODE = get_bool_from_env("DJANGO_MODE")

PROJECT_NAME = "template"

LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.DEBUG)

APPLICATION_HOST=os.environ.get("APPLICATION_HOST", "localhost")
APPLICATION_PORT=get_int_from_env("APPLICATION_PORT")
# endregion

# region openobserve
ENABLE_OPENOBSERVE = get_bool_from_env("ENABLE_OPENOBSERVE")
OPENOBSERVE_HOST = os.environ.get("OPENOBSERVE_HOST")
OPENOBSERVE_PORT = get_int_from_env("OPENOBSERVE_PORT")
OPENOBSERVE_USER = os.environ.get("OPENOBSERVE_USER")
OPENOBSERVE_PASSWORD = os.environ.get("OPENOBSERVE_PASSWORD")
OPENOBSERVE_ORG = os.environ.get("OPENOBSERVE_ORG")
OPENOBSERVE_STREAM = "default"

# region minio
ENABLE_MINIO = get_bool_from_env("ENABLE_MINIO")
MINIO_HOST = os.environ.get("MINIO_HOST")
MINIO_PUBLIC_HOST = os.environ.get("MINIO_PUBLIC_HOST")
MINIO_PORT = get_int_from_env("MINIO_PORT")
MINIO_USER = os.environ.get("MINIO_USER")
MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD")

# region centrifugo
ENABLE_CENTRIFUGO = get_bool_from_env("ENABLE_CENTRIFUGO")
CENTRIFUGO_HOST = os.environ.get("CENTRIFUGO_HOST")
CENTRIFUGO_PORT = get_int_from_env("CENTRIFUGO_PORT")
CENTRIFUGO_TOKEN = os.environ.get("CENTRIFUGO_TOKEN")

# region postgres
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5436")


SQLALCHEMY_DATABASE_URI_BASE = (
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB}"
)


SQLALCHEMY_DATABASE_URI_ASYNC = f"postgresql+asyncpg://{SQLALCHEMY_DATABASE_URI_BASE}"
SQLALCHEMY_DATABASE_URI_SYNC = f"postgresql+psycopg2://{SQLALCHEMY_DATABASE_URI_BASE}"
# endregion


# region prefixes api
API_PREFIX = "/api"


# region поведение системы
DROP_DB_BEFORE_START=get_bool_from_env("DROP_DB_BEFORE_START")

CREATE_TEST_DATA = get_bool_from_env("CREATE_TEST_DATA")
API_USER_TOKEN = os.environ.get("API_USER_TOKEN", None) 
RUN_SSE_LISTNER = get_bool_from_env("RUN_SSE_LISTNER")
# endregion
