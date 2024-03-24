FROM python:3.8
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# Download the model from Google Cloud Storage
RUN apt-get update && apt-get install -y curl \
    && curl -o /app/tmpml/EmpowerMe_emotion_model.h5 "https://storage.cloud.google.com/emotion_ml_model/EmpowerMe_emotion_model.h5" \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]