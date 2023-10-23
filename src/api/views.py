from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import File, Form, Depends, BackgroundTasks
from fastapi import status
from fastapi.responses import Response, RedirectResponse

from container import Container
from servicers import AllureReport, ResultsUnpacker
from .router import AllureReceiverApiRouter

router = AllureReceiverApiRouter()


@router.root
async def root():
    return RedirectResponse('/swagger')


@router.upload_results
@inject
async def upload_results(
        background_tasks: BackgroundTasks,
        file: Annotated[bytes, File(description='Файл архива с результатами тестов в формате AllureReport')],
        trigger_build: Annotated[bool, Form(description='Инициировать сборку отчета после загрузки')] = False,
        unpacker: ResultsUnpacker = Depends(Provide[Container.results_unpacker]),
        allure_report: AllureReport = Depends(Provide[Container.allure_report])
):
    unpacker.execute(file)

    if trigger_build:
        background_tasks.add_task(allure_report.build)

    return Response(
        status_code=status.HTTP_200_OK,
        content='Результаты успешно сохранены'
    )


@router.build_report
@inject
async def build_report(
        background_tasks: BackgroundTasks,
        allure_report: AllureReport = Depends(Provide[Container.allure_report])
):
    background_tasks.add_task(allure_report.build)
    return Response(
        status_code=status.HTTP_200_OK,
        content='Команда на сборку нового отчета принята. Отчет будет сгенерирован в фоновом режиме'
    )


@router.start_ui
@inject
async def start_ui(
        background_tasks: BackgroundTasks,
        allure_report: AllureReport = Depends(Provide[Container.allure_report])
):
    background_tasks.add_task(allure_report.run)
    return Response(
        status_code=status.HTTP_200_OK,
        content='Команда на запуск принята. UI AllureReport будет запущен в фоновом режиме'
    )
