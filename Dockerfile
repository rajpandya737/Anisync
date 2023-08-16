FROM python:3.8
WORKDIR /flask-app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./Anisync ./app
CMD ["python", "./app/app.py"]
