FROM python:3

EXPOSE 5000

COPY . .
RUN pip install -r requirements.txt

#CMD ["gunicorn", "run:subdirectory_app", "--config", "/app/gunicorn.config.py"]
#CMD ["gunicorn", "app:app", "--config", "gunicorn.config.py"]