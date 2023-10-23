from playhouse.db_url import connect

from .base import db_proxy
from .history import History, HistoryItem
from .trends import CategoriesTrend, DurationTrend, HistoryTrend, RetryTrend


def init_database(db_connection_string: str):
    connection = connect(db_connection_string)
    db_proxy.initialize(connection)

    db_proxy.create_tables([
        History,
        HistoryItem,
        CategoriesTrend,
        DurationTrend,
        HistoryTrend,
        RetryTrend
    ])
