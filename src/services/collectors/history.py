import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

from linq import Query

from data.entities import History, HistoryItem
from data.models import TestInfo


class HistoryCollector:
    """Сборщик истории запуска автотестов"""

    def __init__(self, base_path: Path, results_path: Path):
        self.source_path = base_path / 'history.json'
        self.results_path = results_path / 'history.json'

    def collect(self, test_infos: Optional[Dict[str, TestInfo]] = None):
        """Сохранить историю автотестов"""
        with open(self.source_path, 'r') as file:
            file_content = json.load(file)

        histories = list(History.select())

        if test_infos:
            _test_infos = test_infos
        else:
            _test_infos = dict()

        for key, history_data in file_content.items():
            history = Query(histories).first_or_none(lambda h: h.id == key)
            test_info = _test_infos.get(key, None)
            if history:
                self._update_current_history(history, history_data, test_info)
            else:
                self._create_new_history(key, history_data, test_info)

    def extract(self, rebuild: bool = False):
        """Извлечь историю автотестов"""
        histories = History.select()

        content = dict()
        for history in histories:
            content[history.id] = self._create_dict_from_history(history, rebuild)

        with open(self.results_path, 'w') as file:
            json.dump(content, file)

    def _update_current_history(self, history: History, data: Dict[str, Any], test_info: Optional[TestInfo] = None):
        """Обновить историю автотеста

        :param history: текущая история автотеста
        :param data: новые данные истории автотеста
        :param test_info: информация о тесте
        """
        current_items = Query(history.items).select(lambda i: i.uid).to_list()  # type: ignore
        for item in data['items']:
            if item['uid'] in current_items:
                continue

            self._create_history_item_from_dict(history, item)

        history.statistic = data['statistic']

        if test_info:
            history.short_name = test_info.short_name
            history.full_name = test_info.full_name
            history.story = test_info.story
            history.feature = test_info.feature
            history.epic = test_info.epic
            history.tags = test_info.tags
            history.severity = test_info.severity

        history.save()

    def _create_new_history(self, history_id: str, data: Dict[str, Any], test_info: Optional[TestInfo] = None):
        """Создать историю автотеста

        :param history_id: идентификатор автотеста
        :param data: данные истории запуска
        """
        if test_info:
            history = History.create(
                id=history_id,
                statistic=data['statistic'],
                **test_info.model_dump()
            )
        else:
            history = History.create(
                id=history_id,
                statistic=data['statistic']
            )

        for item in data['items']:
            self._create_history_item_from_dict(history, item)

    @staticmethod
    def _create_history_item_from_dict(history: History, data: Dict[str, Any]):
        return HistoryItem.create(
            uid=data['uid'],
            history=history,
            status=data['status'],
            time_start=datetime.fromtimestamp(data['time']['start'] / 1000),
            time_stop=datetime.fromtimestamp(data['time']['stop'] / 1000),
            duration=timedelta(seconds=data['time']['duration']),
            report_url=data.get('reportUrl', None),
            status_details=data.get('statusDetails', None)
        )

    @staticmethod
    def _create_dict_from_history(history: History, rebuild: bool = False):
        history_items = list(
            HistoryItem
            .select()
            .where(HistoryItem.history == history)
            .order_by(HistoryItem.created.desc())  # type: ignore
        )

        if rebuild and len(history_items) > 0:
            history_items[0].delete_instance()
            history_items = history_items[1:]

        return {
            'statistic': history.statistic,
            'items': [
                {
                    'uid': item.uid,
                    'status': item.status,
                    'statusDetails': item.status_details,
                    'reportUrl': item.report_url,
                    'time': {
                        'start': int(item.time_start.timestamp()) * 1000,
                        'stop': int(item.time_stop.timestamp()) * 1000,
                        'duration': int(item.duration.total_seconds()) * 1000
                    }
                } for item in history_items
            ]
        }
