# Use an official Python runtime as a parent image
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python Anisync/app.py
