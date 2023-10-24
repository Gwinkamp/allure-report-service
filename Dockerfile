# Окружение находится в Dockerfile.env
FROM gwinkamp/allure-report-service-env:latest

EXPOSE 8000
EXPOSE 8080

WORKDIR /app
COPY requirements.prod.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY /src .

CMD python main.py