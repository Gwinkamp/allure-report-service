import json
from pathlib import Path

from linq import Query

from data.entities import HistoryTrend


class HistoryTrendCollector:
    """Сборщик статистики длительности автотестов"""

    def __init__(self, base_path: Path, results_path: Path):
        self.source_path = base_path / 'history' / 'history-trend.json'
        self.results_path = results_path / 'history' / 'history-trend.json'

    def collect(self):
        """Сохранить статистику длительности автотестов"""
        with open(self.source_path, 'r') as file:
            file_content = json.load(file)

        item = Query(file_content).first()
        HistoryTrend.create(
            failed=item['data']['failed'],
            broken=item['data']['broken'],
            skipped=item['data']['skipped'],
            passed=item['data']['passed'],
            unknown=item['data']['unknown'],
            total=item['data']['total']
        )

    def extract(self):
        """Извлечь статистику длительности автотестов"""
        trend = (
            HistoryTrend
            .select()
            .order_by(HistoryTrend.created.desc())  # type: ignore
        )

        content = [
            {
                'data': {
                    'failed': t.failed,
                    'broken': t.broken,
                    'skipped': t.skipped,
                    'passed': t.passed,
                    'unknown': t.unknown,
                    'total': t.total
                }
            } for t in trend
        ]

        with open(self.results_path, 'w') as file:
            json.dump(content, file)
