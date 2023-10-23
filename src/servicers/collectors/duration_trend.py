import json
from datetime import timedelta
from pathlib import Path

from linq import Query

from data.entities import DurationTrend


class DurationTrendCollector:
    """Сборщик статистики длительности автотестов"""

    def __init__(self, base_path: Path, results_path: Path):
        self.source_path = base_path / 'history' / 'duration-trend.json'
        self.results_path = results_path / 'history' / 'duration-trend.json'

    def collect(self):
        """Сохранить статистику категорий автотестов"""
        with open(self.source_path, 'r') as file:
            file_content = json.load(file)

        item = Query(file_content).first()
        DurationTrend.create(duration=timedelta(milliseconds=item['data']['duration']))

    def extract(self):
        trend = (
            DurationTrend
            .select()
            .order_by(DurationTrend.created.desc())  # type: ignore
        )

        content = [
            {
                'data': {
                    'duration': int(t.duration.total_seconds() * 100)
                }
            } for t in trend
        ]

        with open(self.results_path, 'w') as file:
            json.dump(content, file)
