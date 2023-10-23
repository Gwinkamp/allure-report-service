from datetime import datetime, timedelta
from uuid import UUID

import peewee
from playhouse.postgres_ext import JSONField, IntervalField

from .base import BaseEntity


class History(BaseEntity):
    id: UUID = peewee.UUIDField(primary_key=True)
    statistic = JSONField()


class HistoryItem(BaseEntity):
    uid: str = peewee.TextField(primary_key=True)
    history = peewee.ForeignKeyField(History, column_name='history_id', backref='items', on_delete='cascade')
    report_url: str = peewee.TextField(null=True)
    status: str = peewee.TextField()
    status_details: str = peewee.TextField(null=True)
    time_start: datetime = peewee.DateTimeField()
    time_stop: datetime = peewee.DateTimeField()
    duration: timedelta = IntervalField()
    created: datetime = peewee.DateTimeField(default=datetime.now)
