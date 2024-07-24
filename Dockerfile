FROM python:3.11-slim

WORKDIR .

COPY requirements.txt .

RUN apt-get update &&  \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config &&  \
    apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./payments ./payments
COPY manage.py .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]