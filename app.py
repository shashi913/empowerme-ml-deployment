from flask import Flask, request
from google.cloud import storage
import numpy as np
from tensorflow.keras.models import load_model
import librosa

app = Flask(__name__)

# Mapping between class IDs and emotion labels
label_mapping = {
    0: 'Angry',
    1: 'Disgusted',
    2: 'Fearful',
    3: 'Happy',
    4: 'Neutral',
    5: 'Sad',
    6: 'Surprised'
}

def load_model_from_gcs(bucket_name, source_blob_name):
    """Loads a model from Google Cloud Storage."""
    storage_client = storage.Client()
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        model_file = blob.download_as_string()
        model = load_model(model_file)
        return model
    except Exception as e:
        print("Error loading model from dcs")

#download_blob('emotion_ml_model', 'EmpowerMe_emotion_model.h5', '/tmpml/EmpowerMe_emotion_model.h5')
model = load_model_from_gcs('emotion_ml_model', 'EmpowerMe_emotion_model.h5')

#model = load_model('E:/IIT/Level_5_year_2/new github commit 21-03-2024/github_latest_22_3_2024/empowerme-ml-deployment/EmpowerMe_emotion_model.h5', compile=False)

# Load the model
#model = load_model('/content/drive/MyDrive/EmpowerMe_emotion_model.h5')
''' # Get the JSON object from the request
data = json.loads(request.data)

# Get the base64 string from the JSON object
base64_str = data['audio']

# Decode the base64 string into bytes
bytes = base64.b64decode(base64_str)

# Write the bytes to a .wav file
with open('temp.wav', 'wb') as f:
    f.write(bytes)'''
@app.route('/predict', methods=['POST'])
def predict():

    # Get audio file and save it
    audio_file = request.files["file"]
    file_name = "temp.wav"
    audio_file.save(file_name)

    # Load audio file and convert it into Mel spectrogram
    audio, _ = librosa.load(file_name, sr=None)
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=_, n_mels=64)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_db_fixed = librosa.util.fix_length(mel_spec_db, size=960)
    mel_spec_db_fixed = np.expand_dims(mel_spec_db_fixed, axis=-1)

    # Predict the class
    prediction = model.predict(np.array([mel_spec_db_fixed]))

    # Get the predicted class ID
    class_id = int(np.argmax(prediction))

    # Get the emotion label corresponding to the class ID
    #emotion_label = label_mapping.get(class_id, 'Unknown')

    # Return the predicted emotion label
    #return emotion_label

    # Print the predicted class ID in the console
    print("Predicted class ID:", class_id)
    
    return str(class_id)

    # Send back the result as json
    #return {"class_id": int(np.argmax(prediction))}

@app.route('/', methods=['GET'])
def home():
    return "Welcome to empowerme emotion recognition model!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
