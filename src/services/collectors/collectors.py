import os
from functools import cached_property
from pathlib import Path

from data.entities import db_proxy
from .categories_trend import CategoriesTrendCollector
from .duration_trend import DurationTrendCollector
from .history import HistoryCollector
from .history_trend import HistoryTrendCollector
from .retry_trend import RetryTrendCollector


class Collectors:

    def __init__(self, build_path: Path, results_path: Path):
        self.base_path = build_path / 'history'
        self.results_path = results_path / 'history'

    @cached_property
    def history(self):
        return HistoryCollector(self.base_path, self.results_path)

    @cached_property
    def history_trend(self):
        return HistoryTrendCollector(self.base_path, self.results_path)

    @cached_property
    def categories_trend(self):
        return CategoriesTrendCollector(self.base_path, self.results_path)

    @cached_property
    def duration_trend(self):
        return DurationTrendCollector(self.base_path, self.results_path)

    @cached_property
    def retry_trend(self):
        return RetryTrendCollector(self.base_path, self.results_path)

    @db_proxy.atomic()
    def collect_all(self):
        """Сохранить историю автотестов"""
        self.history.collect()
        self.history_trend.collect()
        self.categories_trend.collect()
        self.duration_trend.collect()
        self.retry_trend.collect()

    def extract_all(self, rebuild: bool = False):
        """Извлечь историю автотестов в директорию с результатами"""
        if not (self.results_path / 'history').exists():
            os.makedirs(self.results_path / 'history')

        self.history.extract(rebuild)
        self.history_trend.extract(rebuild)
        self.categories_trend.extract(rebuild)
        self.duration_trend.extract(rebuild)
        self.retry_trend.extract(rebuild)
