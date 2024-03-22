FROM python:3.8
WORKDIR /app
ADD . /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
