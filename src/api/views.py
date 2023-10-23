from dependency_injector.wiring import inject, Provide
from fastapi import UploadFile, Form, Depends, BackgroundTasks
from fastapi import status
from fastapi.responses import Response, RedirectResponse

from container import Container
from servicers import AllureReport
from .router import AllureReceiverApiRouter

router = AllureReceiverApiRouter()


@router.root
async def root():
    return RedirectResponse('/swagger')


@router.upload_results
async def upload_results(
        file: UploadFile = Form(description='Файл архива с результатами тестов в формате AllureReport')
):
    return Response(status_code=status.HTTP_200_OK, content=file.filename)


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


@router.terminate_ui
@inject
async def terminate_ui(allure_report: AllureReport = Depends(Provide[Container.allure_report])):
    allure_report.terminate()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
