FROM python:3.8
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "-b", ":8080", "app:app"]
