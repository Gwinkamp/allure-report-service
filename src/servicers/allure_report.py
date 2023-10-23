import logging
import subprocess
from pathlib import Path
from typing import Optional

import config
from .collectors import Collectors


class AllureReport:
    """Класс, инкапсулирующий методы для управления процессом Allure Report"""

    def __init__(
            self,
            host: str,
            port: int,
            results_path: Optional[str] = None,
            build_path: Optional[str] = None,
            allure_path: Optional[str] = None,
    ):
        self.host = host
        self.port = port

        self._results_path = Path(results_path) if results_path else config.ROOT_DIR / 'results'
        self._build_path = Path(build_path) if build_path else config.ROOT_DIR / 'report'
        self._allure_path = Path(allure_path) if allure_path else 'allure'

        self._collectors = Collectors(self._build_path, self._results_path)

        self._process: subprocess.Popen = ...
        self._is_running = False

        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def _open_command(self):
        return (
            f'{self._allure_path} open '
            f'-h {self.host} '
            f'-p {self.port} '
            f'{self._build_path}'
        )

    @property
    def _build_command(self):
        return (
            f'{self._allure_path} generate '
            f'{self._results_path} '
            f'-o {self._build_path} '
            '--clean'
        )

    @property
    def is_running(self):
        return self._is_running

    def run(self):
        if self.is_running:
            self._logger.warning('Команда запуск UI Allure Report проигнорирована, так как UI уже запущен')
            return

        self._logger.info('Выполняется запуск UI Allure Report')
        self._logger.debug(f'Выполнение команды: "{self._open_command}"')

        self._process = subprocess.Popen(
            args=self._open_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        self._is_running = True
        self._process.wait()

        self._is_running = False
        self._logger.critical(
            f'Allure Report завершил свою работу с кодом "{self._process.returncode}". '
            f'STDOUT: {self._process.stdout.read().decode() or "<None>"} '
            f'STDERR: {self._process.stderr.read().decode() or "<None>"}'
        )

    def build(self):
        self._logger.info('Выполняется сборка нового отчета...')

        if self._build_path.exists():
            self._collectors.extract_all()

        self._logger.debug(f'Выполнение команды: "{self._build_command}"')

        process = subprocess.run(
            args=self._build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        if process.returncode != 0:
            logging.error(
                'Сборка нового отчета завершилась с ошибкой. '
                f'STDOUT: {self._process.stdout.read().decode() or "<None>"} '
                f'STDERR: {self._process.stderr.read().decode() or "<None>"}'
            )
            return

        self._collectors.collect_all()
        logging.info('Сборка нового отчета прошла успешно')
