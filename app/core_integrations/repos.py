import base64
import json

import httpx

from lib.utils import get_settings_values, get_settings_value

from . import interfaces


ENABLE_OPENOBSERVE = get_settings_value("ENABLE_OPENOBSERVE")
(ENABLE_OPENOBSERVE, ENABLE_MINIO) = get_settings_values(["ENABLE_OPENOBSERVE", "ENABLE_MINIO"])


if ENABLE_OPENOBSERVE:
    (
    OPENOBSERVE_STREAM,
    OPENOBSERVE_HOST,
    OPENOBSERVE_PORT,
    OPENOBSERVE_USER,
    OPENOBSERVE_PASSWORD,
    OPENOBSERVE_ORG) = get_settings_values([
    "OPENOBSERVE_STREAM",
    "OPENOBSERVE_HOST",
    "OPENOBSERVE_PORT",
    "OPENOBSERVE_USER",
    "OPENOBSERVE_PASSWORD",
    "OPENOBSERVE_ORG"])


    class LoggerRepo(interfaces.LoggerRepoABC):
        def async_client_maker(self) -> httpx.AsyncClient:
            bas64encoded_creds = base64.b64encode(bytes(OPENOBSERVE_USER + ":" + OPENOBSERVE_PASSWORD, "utf-8")).decode("utf-8")
            headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
            base_url = f"http://{OPENOBSERVE_HOST}:{OPENOBSERVE_PORT}/api/{OPENOBSERVE_ORG}"
            client = httpx.AsyncClient(headers=headers, base_url=base_url)
            return client
        
        def client_maker(self) -> httpx.Client:
            bas64encoded_creds = base64.b64encode(bytes(OPENOBSERVE_USER + ":" + OPENOBSERVE_PASSWORD, "utf-8")).decode("utf-8")
            headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
            base_url = f"http://{OPENOBSERVE_HOST}:{OPENOBSERVE_PORT}/api/{OPENOBSERVE_ORG}"
            client = httpx.Client(headers=headers, base_url=base_url)
            return client

        async def log(self, log_data: list[dict[str, str]]) -> None:
            uri = f"/{OPENOBSERVE_STREAM}/_json"
            async with self.async_client_maker() as client:
                response = await client.post(url=uri, content=json.dumps(log_data))
                response

        def sync_log(self, log_data: list[dict[str, str]]) -> None:
            uri = f"/{OPENOBSERVE_STREAM}/_json"
            with self.client_maker() as client:
                response = client.post(url=uri, content=json.dumps(log_data))
                response


else:
    class LoggerRepoMock(interfaces.LoggerRepoABC):
        async def log(self, log_data: list[dict[str, str]]) -> None:
            ...
        
        def sync_log(self, log_data: list[dict[str, str]]) -> None:
            ...
