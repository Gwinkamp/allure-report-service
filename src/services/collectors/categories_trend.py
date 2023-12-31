import json
from pathlib import Path

from linq import Query

from data.entities import CategoriesTrend


class CategoriesTrendCollector:
    """Сборщик статистики категорий автотестов"""

    def __init__(self, base_path: Path, results_path: Path):
        self.source_path = base_path / 'categories-trend.json'
        self.results_path = results_path / 'categories-trend.json'

    def collect(self):
        """Сохранить статистику категорий автотестов"""
        with open(self.source_path, 'r') as file:
            file_content = json.load(file)

        item = Query(file_content).first()
        CategoriesTrend.create(data=item['data'])

    def extract(self, rebuild: bool = False):
        """Извлечь статистику категорий автотестов"""
        trend = list(
            CategoriesTrend
            .select()
            .order_by(CategoriesTrend.created.desc())  # type: ignore
        )

        if rebuild:
            trend[0].delete_instance()
            trend = trend[1:]

        content = [{'data': t.data} for t in trend]

        with open(self.results_path, 'w') as file:
            json.dump(content, file)
