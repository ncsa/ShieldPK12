FROM python:3

EXPOSE 5000

COPY . .

RUN pip install -r requirements.txt

RUN pwd
CMD ["gunicorn", "run:subdirectory_app", "--config", "gunicorn.config.py"]