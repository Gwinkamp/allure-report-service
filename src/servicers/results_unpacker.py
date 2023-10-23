import logging
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from fastapi import status, HTTPException


class ResultsUnpacker:
    """Класс для распаковывания результатов тестов"""

    _BROKEN_ARCHIVE_MSG = 'Переданные данные не являются валидным архивом. Архив поврежден.'
    _INVALID_ARCHIVE_MSG = (
        'Переданные данные не являются валидным архивом. '
        'Результаты тестов необходимо архивировать в zip архив без сжатия'
    )

    def __init__(self, results_path: str):
        self._results_path = Path(results_path)
        self._logger = logging.getLogger(self.__class__.__name__)

    def execute(self, zipped_data: bytes):
        with self.try_read_zip_file(zipped_data) as zip_file:
            self._verify(zip_file)
            zip_file.extractall(self._results_path)

    def try_read_zip_file(self, zipped_data: bytes):
        try:
            return ZipFile(BytesIO(zipped_data), 'r')
        except BadZipFile:
            self._logger.warning(f'Запрос отклонен. Причина: "{self._INVALID_ARCHIVE_MSG}"')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self._INVALID_ARCHIVE_MSG
            )

    def _verify(self, zip_file: ZipFile):
        if zip_file.testzip() is None:
            return

        self._logger.warning(f'Запрос отклонен. Причина: "{self._BROKEN_ARCHIVE_MSG}"')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self._BROKEN_ARCHIVE_MSG
        )
