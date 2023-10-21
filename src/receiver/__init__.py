import config

from .container import Container
from .views import router


def run():
    instance = Container()
    instance.config.from_yaml(config.VALUES_PATH)

    api = instance.api()
    api.include_router(router)

    instance.run_receiver()
