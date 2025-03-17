FROM python:3.10.6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN chmod 644 Anisync/translated_anime_list.sqlite
CMD ["python", "Anisync/app.py"]
EXPOSE 8000
