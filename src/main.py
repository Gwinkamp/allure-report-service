import config
from api import router
from container import Container
from multiprocessing import Process


def main():
    container = Container()
    container.config.from_yaml(config.VALUES_PATH)
    container.config.from_yaml(config.ENV_VALUES_PATH)
    container.init_resources()

    container.wire(['api.views'])

    api = container.api()
    api.include_router(router)

    container.startup()
    container.run_api()


if __name__ == '__main__':
    main()
