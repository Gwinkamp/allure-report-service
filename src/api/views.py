from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import File, Form, Depends, BackgroundTasks
from fastapi import status
from fastapi.responses import Response, RedirectResponse

from container import Container
from services import AllureReport, ResultsUnpacker, ResultsBackuper
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
        rebuild_existing_report: Annotated[bool, Form(description='Пересобрать текущий отчет')] = False,
        allure_report: AllureReport = Depends(Provide[Container.allure_report]),
        unpacker: ResultsUnpacker = Depends(Provide[Container.results_unpacker]),
        backuper: ResultsBackuper = Depends(Provide[Container.results_backuper]),
        backup_to_remote_storage: bool = Depends(Provide[Container.config.features.backup_to_remote_storage])
):
    if not rebuild_existing_report:
        allure_report.clear_results()

    unpacker.execute(file)

    if trigger_build:
        background_tasks.add_task(
            allure_report.build,
            collect_history=True,
            rebuild=rebuild_existing_report
        )

    if backup_to_remote_storage:
        backuper.backup(file)

    return Response(
        status_code=status.HTTP_200_OK,
        content='Результаты успешно сохранены'
    )


@router.build_report
@inject
async def build_report(
        background_tasks: BackgroundTasks,
        collect_history: Annotated[bool, Form(description='Сохранить результаты тестов в историю запусков')] = True,
        allure_report: AllureReport = Depends(Provide[Container.allure_report])
):
    background_tasks.add_task(
        allure_report.build,
        collect_history=collect_history,
        rebuild=False
    )
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
