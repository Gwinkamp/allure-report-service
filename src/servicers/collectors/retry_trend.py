import json
from pathlib import Path

from linq import Query

from data.entities import RetryTrend


class RetryTrendCollector:
    """Сборщик статистики повторов автотестов"""

    def __init__(self, base_path: Path, results_path: Path):
        self.source_path = base_path / 'history' / 'retry-trend.json'
        self.results_path = results_path / 'history' / 'retry-trend.json'

    def collect(self):
        """Сохранить статистику повторов автотестов"""
        with open(self.source_path, 'r') as file:
            file_content = json.load(file)

        item = Query(file_content).first()
        RetryTrend.create(
            run=item['data']['run'],
            retry=item['data']['retry']
        )

    def extract(self):
        """Извлечь статистику повторов автотестов"""
        trend = (
            RetryTrend
            .select()
            .order_by(RetryTrend.created.desc())  # type: ignore
        )

        content = [
            {
                'data': {
                    'run': t.run,
                    'retry': t.retry
                }
            } for t in trend
        ]

        with open(self.results_path, 'w') as file:
            json.dump(content, file)
