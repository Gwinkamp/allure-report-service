import peewee

db_proxy = peewee.DatabaseProxy()


class BaseEntity(peewee.Model):
    class Meta:
        database = db_proxy
        legacy_table_names = False
