from minio import Minio
from centrifuge import Client as _CentrifugoClient


class MinioPubKey(Minio):
    ...


class CentrifugoClient(_CentrifugoClient):
    ...
