import os
import logging
import signal
import subprocess
from pathlib import Path
from typing import Optional

import config


class AllureReport:
    """Класс, инкапсулирующий методы для управления процессом Allure Report"""

    def __init__(
            self,
            host: str,
            port: int,
            build_path: Optional[str] = None,
            allure_path: Optional[str] = None,
    ):
        self.host = host
        self.port = port

        self._build_path = Path(build_path or config.ROOT_DIR / 'report')
        self._allure_path = Path(allure_path) if allure_path else 'allure'

        self._process: subprocess.Popen = ...
        self._is_running = False

        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def command(self):
        return (
            f'{self._allure_path} open '
            f'-h {self.host} '
            f'-p {self.port} '
            f'{self._build_path}'
        )

    @property
    def is_running(self):
        return self._is_running

    def run(self):
        self._logger.info(f'Выполнение команды: "{self.command}"')

        self._process = subprocess.Popen(
            args=self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )

        self._is_running = True
        self._process.wait()

        self._is_running = False
        self._logger.critical(
            f'Allure Report завершил свою работу с кодом "{self._process.returncode}". '
            f'STDOUT: {self._process.stdout.read().decode() or "<None>"} '
            f'STDERR: {self._process.stderr.read().decode() or "<None>"}'
        )

    def terminate(self):
        if not self.is_running:
            self._logger.warning(f'Команда остановки Allure Report проигнорирована, так как процесс и так не запущен')
            return

        self._process.terminate()

        self._is_running = False
        self._logger.info('Процесс Allure Report был остановлен')
