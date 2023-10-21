from fastapi import UploadFile, Form
from fastapi.responses import Response, RedirectResponse

from .router import AllureReceiverApiRouter

router = AllureReceiverApiRouter()


@router.root
async def root():
    return RedirectResponse('/swagger')


@router.upload_results
async def upload_results(
        file: UploadFile = Form(description='Файл архива с результатами тестов в формате AllureReport')
):
    return Response(status_code=200, content=file.filename)


@router.build_report
async def build_report():
    return Response(status_code=200, content='Успех')
