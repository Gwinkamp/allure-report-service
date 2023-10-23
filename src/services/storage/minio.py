import logging
from datetime import datetime
from io import BytesIO

from minio import Minio
from minio.commonconfig import REPLACE, CopySource

from .storage import IStorage


class MinioStorage(IStorage):
    """Файловое хранилище MinIO"""

    def __init__(
            self,
            endpoint: str,
            access_key: str,
            secret_key: str,
            region: str,
            secure: bool,
            bucket_name: str,
            results_path: str
    ):
        self._bucket_name = bucket_name
        self._results_path = results_path
        self._minio = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            secure=secure
        )
        self._logger = logging.getLogger(self.__class__.__name__)

    def upload_results(self, data: bytes):
        package_name = f'results_{datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S-%f")}.zip'
        self._minio.put_object(
            bucket_name=self._bucket_name,
            object_name=f'{self._results_path}/{package_name}',
            content_type='application/zip',
            data=BytesIO(data),
            length=len(data)
        )
        self._minio.copy_object(
            bucket_name=self._bucket_name,
            object_name=f'{self._results_path}/results_latest.zip',
            source=CopySource(
                self._bucket_name,
                f'{self._results_path}/{package_name}'
            ),
            metadata_directive=REPLACE
        )

    def download_results(self):
        try:
            result = self._minio.get_object(
                bucket_name=self._bucket_name,
                object_name=f'{self._results_path}/results_latest.zip'
            )
            return result.data
        except Exception as e:
            self._logger.warning(f'Не удалось восстановить результаты из Minio: {e}')
            return None
