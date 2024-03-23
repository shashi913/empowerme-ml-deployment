FROM python:3.8
WORKDIR /app
COPY . /app
COPY EmpowerMe_emotion_model.h5 /tmpml/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
