FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE $port
CMD ["gunicorn", "-b", ":8080", "app:app"]