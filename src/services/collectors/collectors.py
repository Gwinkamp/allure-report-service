import logging
import os
from functools import cached_property
from pathlib import Path
from typing import Dict

from data.entities import db_proxy
from data.models import TestInfo
from .categories_trend import CategoriesTrendCollector
from .duration_trend import DurationTrendCollector
from .history import HistoryCollector
from .history_trend import HistoryTrendCollector
from .results import ResultsCollector
from .retry_trend import RetryTrendCollector


class Collectors:

    def __init__(self, build_path: Path, results_path: Path, save_test_infos: bool = False):
        self.results_path = results_path
        self.history_base_path = build_path / 'history'
        self.history_results_path = results_path / 'history'
        self.logger = logging.getLogger('collectors')
        self.save_test_infos = save_test_infos

    @cached_property
    def history(self):
        return HistoryCollector(self.history_base_path, self.history_results_path)

    @cached_property
    def history_trend(self):
        return HistoryTrendCollector(self.history_base_path, self.history_results_path)

    @cached_property
    def categories_trend(self):
        return CategoriesTrendCollector(self.history_base_path, self.history_results_path)

    @cached_property
    def duration_trend(self):
        return DurationTrendCollector(self.history_base_path, self.history_results_path)

    @cached_property
    def retry_trend(self):
        return RetryTrendCollector(self.history_base_path, self.history_results_path)

    @cached_property
    def results(self):
        return ResultsCollector(self.results_path)

    @db_proxy.atomic()
    def collect_all(self):
        """Сохранить историю автотестов"""
        test_infos: Dict[str, TestInfo] = dict()
        if self.save_test_infos:
            test_infos = self._collect_results()

        self.history.collect(test_infos)
        self.history_trend.collect()
        self.categories_trend.collect()
        self.duration_trend.collect()
        self.retry_trend.collect()

    def extract_all(self, rebuild: bool = False):
        """Извлечь историю автотестов в директорию с результатами"""
        if not self.history_results_path.exists():
            os.makedirs(self.history_results_path)

        self.history.extract(rebuild)
        self.history_trend.extract(rebuild)
        self.categories_trend.extract(rebuild)
        self.duration_trend.extract(rebuild)
        self.retry_trend.extract(rebuild)

    def _collect_results(self) -> Dict[str, TestInfo]:
        try:
            self.results.collect()
            return self.results.data
        except Exception as e:
            self.logger.error(f'Ошибка разбора результатов тестов: {e}', exc_info=True)
            return dict()
