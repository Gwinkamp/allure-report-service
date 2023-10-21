import uvicorn

from fastapi import FastAPI
from dependency_injector import providers


class Container(providers.DependenciesContainer):

    config = providers.Configuration()

    api = providers.Singleton(
        FastAPI,
        debug=config.debug,
        title='Allure Receiver',
        summary='Приёмник результатов тестирования',
        description='Сервис приёма результатов тестирования извне для последующей их передачи в AllureReport',
        version='0.0.1',
        docs_url='/swagger'
    )

    run_receiver = providers.Callable(
        uvicorn.run,
        app=api,
        host=config.host,
        port=config.port
    )
