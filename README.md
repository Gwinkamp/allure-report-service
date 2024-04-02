# allure-report-service

Сервис AllureReport для отображения результатов тестирования

## Зависимости

Для запуска сервиса достаточно зависимостей из файла `requirements.prod.txt`:

```shell
pip install -r requirements.prod.txt
```

Для использования вспомогательных инструментов 
([mypy](https://github.com/python/mypy) и [flake8](https://flake8.pycqa.org/en/latest/index.html)) 
нужно установить зависимости из `requirements.dev.txt`.  

Также необходима утилита [allure](https://allurereport.org/docs/gettingstarted-installation/).

## Запуск

### Конфигурация

Перед стартом сервиса нужно задать переменную окружения `DEBUG` - признак запуска в режиме отладки. Принимает значения: `true` или `false`.  
Настройки конфигурации находятся в файлах:

* `src/values.yaml`
* `src/values.debug.yaml` - при условии `DEBUG=true`
* `src/values.production.yaml` - при условии `DEBUG=false`

Также конфигурацию можно настроить с помощью переменных окружения (название переменных см. в yaml)

### Доступ к БД

Данный сервис записывает историю результатов тестов Allure Report в БД для возможности удобной очистки истории по дате. 
Поддерживается только Postgres, так как используются типы полей `Interval` и `JSON`. Адрес до БД устанавливается в yaml настройках конфигурации.

Перед первым стартом сервиса в Postgres необходимо создать БД, если она еще не была создана. Все необходимые таблицы сервис создаст сам при первом запуске.

### Дополнительные фичи

Переключатели находятся в `values.*.yaml` в `features`

#### Доступ к удаленному хранилищу

Данный сервис может сохранять пакеты с результатами тестов в удаленное хранилище. На данный момент поддерживается только тип хранилища MinIO. 
Для включения/отключения данной фичи используется bool параметр `features.backup_to_remote_storage` в yaml настройках конфигурации. Данные для подключения к хранилищу находятся там же.

#### Сохранение данных автотестов

Данная фича будет полезна тем, кого не устраивают дефолтные метрики Allure Report и кто хочет настроить свои метрики и графики где-нибудь в Grafana. 
После включения данной фичи, при каждой публикации результатов тестов, будут прочитаны все файлы с этими результатами и их данные будут сохранены в БД. 
Это нужно для более детализированных метрик.  

Для включения/отключения данной фичи используется bool параметр `features.save_test_infos` в yaml настройках конфигурации.

### Локальный запуск

Выполнить команду и директории `src`:

```shell
python main.py
```

### Запуск из Docker

Ссылка на docker образ: https://hub.docker.com/r/gwinkamp/allure-report-service

```shell
docker run -e DEBUG=false -e DB_CONNECTION_STRING=postgresext://postgres:postgres@localhost:5432/allure_history -p 8000:8000 -p 8080:8080 gwinkamp/allure-report-service:latest
```

## Работа с сервисом

после успешного старта сервиса запустятся два процесса:

1. Allure Report - UI интерфейс Allure Report на порту `ui_port` в yaml настройках конфигурации
2. Allure Receiver - API приёмника результатов тестов на порту `api_port` в yaml настройках конфигурации

При переходе в Allure Receiver в браузере открывается swagger документация, где есть следующие методы:

#### `[POST] /results/upload` 

Метод для загрузки результатов тестов.  

Входные параметры:
* `file` - zip архив результатами тестов в формате Allure Report;
* `trigger_build` - признак сборки отчета после загрузки архива с тестами. Если true, то сервис выполняет команду генерации отчета с переданными результатами тестов. Отчет после сборки отображается в UI Allure Report;
* `rebuild_existing_report` - признак пересборки текущего отчета. Если true, то сервис перезапишет последний отчет в истории результатов тестов. Последние результаты тестов не потеряются, а уйдут во вкладку Retries в UI Allure Report;

Возвращает строку с сообщением об успехе.

#### `[PUT] /report/build`

Метод сборки отчета с результатами тестов. Используется для пересборки отчета в случае непредвиденного сбоя.  

Входные параметры:
* `collect_history` - признак, указывающий на необходимость сохранить результаты сгенерированного отчета в историю.

Возвращает строку с сообщением об успехе.

#### `[POST] /report/start`

Метод запуска UI Allure Report. Используется для в случе непредвиденного сбоя в UI. Не имеет входных параметров.  
Возвращает строку с сообщением об успехе.

## Полезные инструменты:

Для публикации результатов тестов есть готовый модуль на python: [allure-results-publisher](https://github.com/Gwinkamp/allure-results-publisher).
