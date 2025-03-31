import asyncio
import os
import sys
import pathlib
from types import ModuleType


DIRECTORY_PATH = pathlib.Path.cwd()
sys.path.insert(1, DIRECTORY_PATH.as_posix())

from archtool.dependency_injector import DependencyInjector

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from lib.middlewares import my_exception_handler

from app.config import APPLICATION_HOST, APPLICATION_PORT, ENABLE_CENTRIFUGO, PROJECT_NAME, ENABLE_OPENOBSERVE
from app.archtool_conf.bundle_project import bundle
from app.core_integrations.dep_keys import CentrifugoClient


def register_router(app: FastAPI, module: ModuleType) -> None:
    app.include_router(module.router)


def create_app(name: str = PROJECT_NAME) -> tuple[FastAPI, DependencyInjector]:
    application = FastAPI(title=name)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    injector = bundle(app=application)

    if ENABLE_OPENOBSERVE:
        # подключаем обработку ошибок. При 500 лог будет сохраняться в openobserve
        application.exception_handler(Exception)(my_exception_handler)

    # пример запуска асинхронной задачи
    subtasks = []
    if ENABLE_CENTRIFUGO:
        centrifugo_client = injector.get_dependency(CentrifugoClient)
        subtasks.append(centrifugo_client.connect())

    @application.on_event("startup")
    async def startup_event():
        for task in subtasks:
            asyncio.create_task(task)

    return application, injector


if __name__ == "__main__":
    app, injector = create_app()
    uvicorn.run(
        app,
        host=APPLICATION_HOST,
        port=APPLICATION_PORT
        )
