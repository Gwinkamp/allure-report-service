from functools import cached_property

from fastapi import APIRouter


class AllureReceiverApiRouter(APIRouter):

    @cached_property
    def root(self):
        return self.get('/', include_in_schema=False)

    @cached_property
    def upload_results(self):
        return self.post(
            '/results/upload',
            response_model=str,
            tags=['results'],
            summary='Загрузить результаты тестирования'
        )

    @cached_property
    def build_report(self):
        return self.put(
            '/report/build',
            response_model=str,
            tags=['report'],
            summary='Построить отчет о результатах тестирования'
        )

    @cached_property
    def start_ui(self):
        return self.post(
            '/report/start',
            response_model=str,
            tags=['report'],
            summary='Запустить UI AllureReport'
        )
