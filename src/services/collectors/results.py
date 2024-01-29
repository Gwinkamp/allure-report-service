import json
from pathlib import Path
from typing import Dict, List, Optional

from linq import Query

from data.models import TestInfo


class ResultsCollector:
    """Сборщик результатов автотестов"""

    def __init__(self, results_path: Path):
        self.results_path = results_path

        # сопоставление historyId с данными теста
        self.data: Dict[str, TestInfo] = dict()

    def collect(self):
        for path in self.results_path.glob('*-result.json'):
            self._collect_from_file(path)

    def _collect_from_file(self, path: Path):
        with open(path, 'r') as file:
            data = json.load(file)

        key = data['historyId']
        labels = data.get('labels', [])

        self.data[key] = TestInfo(
            short_name=data['name'],
            full_name=data.get('fullName', None),
            story=self._get_from_label(labels, 'story'),
            feature=self._get_from_label(labels, 'feature'),
            epic=self._get_from_label(labels, 'epic'),
            severity=self._get_from_label(labels, 'severity'),
            tags=(
                Query(labels)
                .where(lambda x: x['name'] == 'tag')
                .select(lambda x: x['value'])
                .to_list()
            )
        )

    @staticmethod
    def _get_from_label(labels: List[Dict[str, str]], name: str) -> Optional[str]:
        return (
            Query(labels)
            .where(lambda x: x['name'] == name)
            .select(lambda x: x['value'])
            .first_or_none()
        )
