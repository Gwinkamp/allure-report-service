from datetime import datetime, timedelta
from uuid import UUID

import peewee
from playhouse.postgres_ext import JSONField, IntervalField

from .base import BaseEntity


class CategoriesTrend(BaseEntity):
    id: UUID = peewee.UUIDField(primary_key=True)
    data: str = JSONField()
    created: datetime = peewee.DateTimeField(default=datetime.now)


class DurationTrend(BaseEntity):
    id: UUID = peewee.UUIDField(primary_key=True)
    duration: timedelta = IntervalField()
    created: datetime = peewee.DateTimeField(default=datetime.now)


class RetryTrend(BaseEntity):
    id: UUID = peewee.UUIDField(primary_key=True)
    run: int = peewee.IntegerField()
    retry: int = peewee.IntegerField()
    created: datetime = peewee.DateTimeField(default=datetime.now)


class HistoryTrend(BaseEntity):
    id: UUID = peewee.UUIDField(primary_key=True)
    failed: int = peewee.IntegerField()
    broken: int = peewee.IntegerField()
    skipped: int = peewee.IntegerField()
    passed: int = peewee.IntegerField()
    unknown: int = peewee.IntegerField()
    total: int = peewee.IntegerField()
    created: datetime = peewee.DateTimeField(default=datetime.now)
