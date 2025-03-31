from io import BytesIO
import json
import os
from typing import Any
import aiohttp
import datetime
from pathlib import Path
import importlib

from fastapi import Request

from .env_helpers import get_bool_from_env


def get_settings_value(key: str):
    project_name = Path.cwd().name
    if get_bool_from_env("DJANGO_MODE"):
        settings = importlib.import_module(f"{project_name}.settings")
    else:
        from app import config as settings
    result = getattr(settings, key)
    return result


def get_settings_values(keys: list[str]) -> list[Any]:
    project_name = Path.cwd().name
    if get_bool_from_env("DJANGO_MODE"):
        settings = importlib.import_module(f"{project_name}.settings")
    else:
        from app import config as settings
    result = [getattr(settings, key) for key in keys]
    return result


async def download_large_file(url: str,
                              save_dir: Path) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: {response.status}")
            cd_header = response.headers.get('Content-Disposition')
            if cd_header:
                filename = cd_header.split('filename=')[-1].strip('\"')
            else:
                filename = Path(url).name
            extension = filename.split(".")[1]
            filename = f"{datetime.now()}.{extension}".replace(" ", "_")
            save_path = Path(save_dir) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(1024 * 1024):  # 1 MB chunks
                    f.write(chunk)
            return filename

def map_to_dict(keys, values, **kwargs):
    for value in values:
        prepared = dict(zip(keys, value))
        for key, generator in kwargs.items():
            prepared[key] = list(generator(prepared[key]))
        yield prepared

async def serialize_fastapi_request(request: Request) -> dict:
    request_serialized = {}
    # Считываем тело запроса в байтах
    # Попытаемся распарсить его как JSON, если не получится, оставим как строку
    try:
        body_bytes = ""
        body_bytes = await request.body()
        try:
            body = json.loads(body_bytes)
        except json.JSONDecodeError:
            body = body_bytes.decode("utf-8")
    except Exception as ex:
        body = None

    # Составляем структуру для лога
    request_serialized = {
        "method": request.method,
        "url": str(request.url),  # URL целиком, включая query-параметры
        "headers": str(dict(request.headers)),
        "cookies": request.cookies,
        "query_params": str(dict(request.query_params)),
        "path_params": request.path_params,
        "body": body}
    return request_serialized

