from functools import cached_property

from fastapi import APIRouter


class AllureReceiverApiRouter(APIRouter):

    @cached_property
    def root(self):
        return self.get('/', include_in_schema=False)

    @cached_property
    def upload_results(self):
        return self.post(
            '/upload',
            response_model=str,
            tags=['main'],
            summary='Загрузить результаты тестирования'
        )

    @cached_property
    def build_report(self):
        return self.put(
            '/build',
            response_model=str,
            tags=['main'],
            summary='Построить отчет о результатах тестирвоания'
        )
