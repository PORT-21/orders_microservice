import asyncio
import pathlib

from archtool.dependency_injector import DependencyInjector
from archtool.global_types import AppModule
from app.archtool_conf.custom_layers import APPS, app_layers, RoutersInitializationStrategyABC

from fastapi import FastAPI

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker)


import app.config as settings
from app.core_integrations.reg_deps import reg_deps

from lib.building_utils import import_all_models, run_endpoints_initializers
from lib.db import Base
from lib.db import init_db


from sqlalchemy.pool import NullPool


def init_deps(injector: DependencyInjector) -> AsyncEngine:
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI_ASYNC,
                                 echo=True,
                                 poolclass=NullPool)
    session_maker = async_sessionmaker(bind=engine,
                                       class_=AsyncSession,
                                       expire_on_commit=False)

    # from sqlalchemy import create_engine, Engine
    # from sqlalchemy.orm import sessionmaker, scoped_session

    injector._reg_dependency(AsyncEngine, engine, use_serialization_function=True, nested_injections_allowed=False)
    injector._reg_dependency(async_sessionmaker, session_maker, use_serialization_function=True, nested_injections_allowed=False)
    reg_deps(injector)
    return engine



def bundle(app: FastAPI) -> DependencyInjector:
    import sys
    apps_root = pathlib.Path.cwd() / 'app'
    sys.path.insert(0, apps_root.as_posix())
    injector = DependencyInjector(modules_list=APPS, layers=app_layers)
    engine = init_deps(injector=injector)
    import_all_models(Base=Base)
    injector.inject()
    run_endpoints_initializers(injector=injector, app=app)
    
    db_task =\
        init_db(Base,
                settings.SQLALCHEMY_DATABASE_URI_ASYNC,
                engine=engine,
                drop_db=settings.DROP_DB_BEFORE_START)

    try:
        loop = asyncio.get_running_loop()
        loop.run_until_complete(db_task)
    except Exception:
        asyncio.run(db_task)

    return injector
