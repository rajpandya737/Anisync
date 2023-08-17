FROM python:3.10.6
WORKDIR /flask-app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./Anisync ./app
RUN chmod 644 ./app/translated_anime_list.sqlite
CMD ["python", "./app/app.py"]
