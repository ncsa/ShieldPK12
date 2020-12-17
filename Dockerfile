FROM python:3

EXPOSE 5000

WORKDIR /app

COPY . .

RUN pip install -r /app/requirements.txt

RUN pwd
CMD []
