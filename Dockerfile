FROM python:3.8

# Install Google Cloud SDK and gsutil
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get update && apt-get install -y google-cloud-sdk

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Download the model file from Google Cloud Storage
RUN echo "Downloading model file from Google Cloud Storage..."
RUN gsutil cp gs://emotion_ml_model/EmpowerMe_emotion_model.h5 /tmpml/

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Command to run the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
