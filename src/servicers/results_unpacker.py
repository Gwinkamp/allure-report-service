from io import BytesIO
from pathlib import Path
from zipfile import ZipFile


class ResultsUnpacker:
    """Класс для распаковывания реузльтатов тестов"""

    def __init__(self, results_path: str):
        self._results_path = Path(results_path)

    def execute(self, zipped_data: bytes):
        with ZipFile(BytesIO(zipped_data)) as zf:
            zf.extractall(self._results_path)
