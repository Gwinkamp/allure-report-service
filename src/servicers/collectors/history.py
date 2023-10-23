import json
from pathlib import Path
from typing import Optional
from uuid import UUID

from linq import Query

import config
from data.entities import History, HistoryItem


class HistoryCollector:

    def __init__(self, build_path: Optional[str] = None):
        self._build_path = Path(build_path) if build_path else config.ROOT_DIR / 'report'

    def collect_history(self):
        ...

    def _collect_from_history_file(self):
        with open(self._build_path / 'history' / 'history.json', 'r') as file:
            file_content = json.load(file)

        histories = list(History.select().join(HistoryItem))

        for key, current in file_content.items():
            history = Query(histories).first_or_none(lambda h: h.id == UUID(key))

            # если уже есть в БД
            if history:
                current_items = Query(history.items).select(lambda i: i.uid).to_list()
                for item in current['items']:
                    if not item['uid'] in current_items:
                        HistoryItem.create(
                            uid=item['uid'],
                            history=history,
                            status=item['status'],
                            time_start=item['time']['start'],
                            time_stop=item['time']['stop'],
                            duration=item['time']['duration'],
                            report_url=item.get('reportUrl', None),
                            status_details=item.get('statusDetails', None)
                        )
                history.statistic = json.dumps(current['statistic'])
                history.save()
            # новая история
            else:
                new_history = History.create(
                    id=UUID(key),
                    statistic=json.dumps(current['statistic'])
                )
                for item in current['items']:
                    HistoryItem.create(
                        uid=item['uid'],
                        history=new_history,
                        status=item['status'],
                        time_start=item['time']['start'],
                        time_stop=item['time']['stop'],
                        duration=item['time']['duration'],
                        report_url=item.get('reportUrl', None),
                        status_details=item.get('statusDetails', None)
                    )

        # for history in History.select().join(HistoryItem):
        #     current = file_content.get(history.id.hex, None)
        #     if current:
        #         current_items = Query(history.items).select(lambda i: i.uid).to_list()
        #         for item in current['items']:
        #             if not item['uid'] in current_items:
        #                 HistoryItem.create(
        #                     uid=item['uid'],
        #                     history=history,
        #                     status=item['status'],
        #                     time_start=item['time']['start'],
        #                     time_stop=item['time']['stop'],
        #                     duration=item['time']['duration'],
        #                     report_url=item.get('reportUrl', None),
        #                     status_details=item.get('statusDetails', None)
        #                 )
