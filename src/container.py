import logging.config
import os

import rich
import uvicorn
from dependency_injector import containers, providers
from fastapi import FastAPI

from config import ROOT_DIR
from data.entities import init_database
from services import AllureReport, ResultsUnpacker, MinioStorage, ResultsBackuper
from startup import startup


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

    make_build_path = providers.Resource(
        os.makedirs,
        name=config.allure.build_path,
        exist_ok=True,
    )

    make_results_path = providers.Resource(
        os.makedirs,
        name=config.allure.results_path,
        exist_ok=True,
    )

    api = providers.Singleton(
        FastAPI,
        debug=config.debug,
        title='Allure Receiver',
        summary='Приёмник результатов тестирования',
        description='Сервис приёма результатов тестирования извне для последующей их передачи в AllureReport',
        version='1.0.3',
        docs_url='/swagger'
    )

    allure_report = providers.Singleton(
        AllureReport,
        host=config.ui_host,
        port=config.ui_port,
        allure=config.allure.script_path,
        build_path=config.allure.build_path,
        results_path=config.allure.results_path,
        save_test_infos=config.features.save_test_infos
    )

    results_unpacker = providers.Singleton(
        ResultsUnpacker,
        results_path=config.allure.results_path
    )

    minio = providers.Singleton(
        MinioStorage,
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        region=config.minio.region,
        secure=config.minio.secure,
        bucket_name=config.minio.bucket_name,
        results_path=config.minio.results_path
    )

    results_backuper = providers.Singleton(
        ResultsBackuper,
        storage=minio,
        unpacker=results_unpacker
    )

    startup = providers.Callable(
        startup,
        allure_report=allure_report,
        backuper=results_backuper,
        results_path=config.allure.results_path,
        backup_to_remote_storage=config.features.backup_to_remote_storage
    )

    run_api = providers.Callable(
        uvicorn.run,
        app=api,
        host=config.api_host,
        port=config.api_port,
        log_config=str(ROOT_DIR / 'logging.ini')
    )
