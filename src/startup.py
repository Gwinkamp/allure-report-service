import os
from threading import Thread

from services import AllureReport, ResultsBackuper


def startup(
        allure_report: AllureReport,
        backuper: ResultsBackuper,
        results_path: str,
        backup_to_remote_storage: bool
):
    """Скрипт для запуска allure report при старте сервиса"""
    if backup_to_remote_storage:
        restored = restore_results(backuper, results_path)
        if restored:
            allure_report.build(collect_history=False)

    allure_thread = Thread(target=allure_report.run)
    allure_thread.start()


def restore_results(backuper: ResultsBackuper, results_path: str):
    """Скрипт восстановления результатов тестов из удаленного хранилища перед запуском сервиса"""
    if len(os.listdir(results_path)) != 0:
        return False

    return backuper.restore()
