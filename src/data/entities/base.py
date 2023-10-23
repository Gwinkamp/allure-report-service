import peewee

db_proxy = peewee.DatabaseProxy()


class BaseEntity(peewee.Model):
    class Config:
        database = db_proxy
