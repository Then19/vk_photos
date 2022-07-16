FROM python:3.9

WORKDIR /app
EXPOSE 80

ENV CLICKHOUSE_DSN=""

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]
