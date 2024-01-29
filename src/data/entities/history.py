from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import peewee
from playhouse.postgres_ext import JSONField, IntervalField, ArrayField

from .base import BaseEntity


class History(BaseEntity):
    id: str = peewee.TextField(primary_key=True)
    statistic: Dict[str, Any] = JSONField()
    short_name: Optional[str] = peewee.TextField(null=True, default=None)
    full_name: Optional[str] = peewee.TextField(null=True, default=None)
    story: Optional[str] = peewee.TextField(null=True, default=None)
    feature: Optional[str] = peewee.TextField(null=True, default=None)
    epic: Optional[str] = peewee.TextField(null=True, default=None)
    tags: List[str] = ArrayField(peewee.TextField, default=[])
    severity: Optional[str] = peewee.TextField(null=True, default=None)


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
