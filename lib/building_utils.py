import pathlib
from typing import TypeVar
from inspect import isclass, signature

from archtool.dependency_injector import DependencyInjector
from archtool.utils import get_subclasses_from_module

from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeBase

from .utils import get_settings_value

if get_settings_value("DJANGO_MODE"):
    # from django.apps import apps
    # from django.urls import path
    # from metall_crm.settings import INSTALLED_APPS
    from apps.archtool_bundle.layers import RoutersInitializationStrategyABC

else:
    from app.archtool_conf.custom_layers import APPS
    from app.archtool_conf.custom_layers import RoutersInitializationStrategyABC


from typing import Callable


T = TypeVar("T")


def run_endpoints_initializers(injector: DependencyInjector, app: FastAPI):
    initializers = filter_objects_of_type(injector, RoutersInitializationStrategyABC)
    for initializer in initializers:
        initializer()
        app.include_router(initializer.router)


def filter_objects_of_type(injector: DependencyInjector, obj_type: T) -> list[T]:
    result = []
    for key, value in injector._dependencies.items():
        if isclass(type(value)) and isinstance(value, obj_type):
            result.append(value)
    return result


def run_endpoints_initializers(injector: DependencyInjector, app: FastAPI):
    initializers = filter_objects_of_type(injector, RoutersInitializationStrategyABC)
    for initializer in initializers:
        initializer()
        app.include_router(initializer.router)


def get_fastapi_app():
    ...


def import_all_models(Base) -> list[DeclarativeBase]:
    all_models = []
    for app in APPS:
        modules_path = "." / pathlib.Path(app.import_path.replace('.', '/')) / 'models.py' 
        if not modules_path.exists(): continue
        import_path = f"{app.import_path}.models"
        models = get_subclasses_from_module(module_path=import_path, superclass=Base)
        all_models.extend(models)
    return list(set(all_models))



def create_functional_wrapper(handler: Callable, controller) -> Callable:
    def wrapper(*args, **kwargs):
        # self=controller, 
        return handler(*args, **kwargs)
    mock_signature = signature(handler)
    wrapper.name = handler.name
    wrapper.signature = mock_signature
    return wrapper
