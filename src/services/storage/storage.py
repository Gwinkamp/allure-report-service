from abc import ABCMeta, abstractmethod


class IStorage(metaclass=ABCMeta):
    """Интерфейс удаленного хранилища"""

    @abstractmethod
    def upload_results(self, data: bytes) -> None:
        ...

    @abstractmethod
    def download_results(self) -> bytes | None:
        ...
