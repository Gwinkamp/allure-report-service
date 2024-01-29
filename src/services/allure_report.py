import logging
import os
import shutil
import subprocess
from pathlib import Path

from data import db_proxy
from .collectors import Collectors


class AllureReport:
    """Класс, инкапсулирующий методы для управления процессом Allure Report"""

    def __init__(
            self,
            host: str,
            port: int,
            allure: str,
            results_path: str,
            build_path: str,
            save_test_infos: bool = False,
    ):
        self.host = host
        self.port = port

        self._allure = allure
        self._results_path = Path(results_path)
        self._build_path = Path(build_path)

        self._is_running = False
        self._logger = logging.getLogger(self.__class__.__name__)
        self._collectors = Collectors(self._build_path, self._results_path, save_test_infos)

    @property
    def _open_command(self):
        return (
            f'{self._allure} open '
            f'-h {self.host} '
            f'-p {self.port} '
            f'{self._build_path}'
        )

    @property
    def _build_command(self):
        return (
            f'{self._allure} generate '
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

        process = subprocess.Popen(
            args=self._open_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        self._is_running = True
        process.wait()

        self._is_running = False
        self._logger.critical(
            f'Allure Report завершил свою работу с кодом "{process.returncode}". '
            f'STDOUT: {process.stdout.read().decode() or "<None>" if process.stdout else "<None>"} '
            f'STDERR: {process.stderr.read().decode() or "<None>" if process.stderr else "<None>"}'
        )

    @db_proxy.connection_context()
    def build(self, collect_history: bool = True, rebuild: bool = False):
        self._logger.info('Выполняется сборка нового отчета...')

        if self._collectors.history_base_path.exists():
            self._collectors.extract_all(rebuild)

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
                f'STDOUT: {process.stdout.decode() or "<None>"} '
                f'STDERR: {process.stderr.decode() or "<None>"}'
            )
            return

        if collect_history:
            self._collectors.collect_all()

        logging.info('Сборка нового отчета прошла успешно')

    def clear_results(self):
        shutil.rmtree(self._results_path)
        os.makedirs(self._results_path)
