import logging.config

import rich
import uvicorn
from dependency_injector import containers, providers
from fastapi import FastAPI

from config import ROOT_DIR
from servicers import AllureReport
from data.entities import init_database


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    init_logging = providers.Resource(
        logging.config.fileConfig,
        fname=ROOT_DIR / 'logging.ini'
    )

    reconfigure_logging = providers.Resource(
        rich.reconfigure,
        width=256
    )

    init_database = providers.Resource(
        init_database,
        db_connection_string=config.db_connection_string
    )

    api = providers.Singleton(
        FastAPI,
        debug=config.debug,
        title='Allure Receiver',
        summary='Приёмник результатов тестирования',
        description='Сервис приёма результатов тестирования извне для последующей их передачи в AllureReport',
        version='0.0.1',
        docs_url='/swagger'
    )

    allure_report = providers.Singleton(
        AllureReport,
        host=config.ui_host,
        port=config.ui_port,
        allure=config.allure.script_path,
        build_path=config.allure.build_path,
        results_path=config.allure.results_path
    )

    run_api = providers.Callable(
        uvicorn.run,
        app=api,
        host=config.api_host,
        port=config.api_port,
        log_config=str(ROOT_DIR / 'logging.ini')
    )
