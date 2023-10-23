import logging

from .results_unpacker import ResultsUnpacker
from .storage import IStorage


class ResultsBackuper:
    """Класс, осуществляющий резервное копирование результатов автотестов на удаленное хранилище"""

    def __init__(
            self,
            storage: IStorage,
            unpacker: ResultsUnpacker
    ):
        self._storage = storage
        self._unpacker = unpacker
        self._logger = logging.getLogger(self.__class__.__name__)

    def backup(self, data: bytes):
        self._logger.info(f'Загрузка результатов тестов в удаленное хранилище "{self._storage.__class__.__name__}"')

        self._storage.upload_results(data)

    def restore(self):
        self._logger.info(f'Скачивание результатов тестов из удаленного хранилища "{self._storage.__class__.__name__}"')

        data = self._storage.download_results()
        if data:
            self._unpacker.execute(data)
            return True

        return False
