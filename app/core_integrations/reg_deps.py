from archtool.dependency_injector import DependencyInjector
from minio import Minio
from centrifuge import Client as _CentrifugoClient
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from lib.utils import get_settings_values

from .centrifugo_deps import ClientEventLoggerHandler, get_client_token
from .dep_keys import MinioPubKey, CentrifugoClient


def reg_deps(injector: DependencyInjector):
    (
    ENABLE_MINIO,
    MINIO_HOST,
    MINIO_PUBLIC_HOST,
    MINIO_PORT,
    MINIO_USER,
    MINIO_PASSWORD) = get_settings_values([
    "ENABLE_MINIO",
    "MINIO_HOST",
    "MINIO_PUBLIC_HOST",
    "MINIO_PORT",
    "MINIO_USER",
    "MINIO_PASSWORD"])

    (
    ENABLE_CENTRIFUGO,
    CENTRIFUGO_HOST,
    CENTRIFUGO_PORT) = get_settings_values([
    "ENABLE_CENTRIFUGO",
    "CENTRIFUGO_HOST",
    "CENTRIFUGO_PORT"])

    if ENABLE_MINIO:
        MINIO_CLIENT = Minio(
                    f"{MINIO_HOST}:{MINIO_PORT}",
                    access_key=MINIO_USER,
                    secret_key=MINIO_PASSWORD,
                    secure=False)

        MINIO_PUB_CLIENT = Minio(
                f"{MINIO_PUBLIC_HOST}:{MINIO_PORT}",
                access_key=MINIO_USER,
                secret_key=MINIO_PASSWORD,
                secure=False)

        injector._reg_dependency(Minio, MINIO_CLIENT)
        injector._reg_dependency(MinioPubKey, MINIO_PUB_CLIENT)

    if ENABLE_CENTRIFUGO:
        centrifugo_client = _CentrifugoClient(
            f"ws://{CENTRIFUGO_HOST}:{CENTRIFUGO_PORT}/connection/websocket",
            events=ClientEventLoggerHandler(),
            get_token=get_client_token,
            use_protobuf=False,
        )
        injector._reg_dependency(CentrifugoClient, centrifugo_client)


    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
