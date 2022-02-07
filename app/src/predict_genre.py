import json
import math
import os

import librosa
import numpy as np
from keras.models import load_model
from pydub import AudioSegment
import random
from collections import Counter

JSON_PATH = "predict.json"

trainModel = load_model('MGCmodel/trainModel.h5')

genres = {
    0: 'blues',
    1: 'classical',
    2: 'country',
    3: 'disco',
    4: 'hip-hop',
    5: 'jazz',
    6: 'metal',
    7: 'pop',
    8: 'reggae',
    9: 'rock'
}


# function to find the most frequent element of an array
def most_frequent(l):
    occurrence = Counter(l)
    return occurrence.most_common(1)[0][0]


def save_mfcc(filePath, jsonPath, nMfcc=13, nFft=2048, hopLength=512, numSegments=10):
    # dictionary to store data to predict
    data = {
        "mfcc": []  # inputs
    }
    
    """if filePath.endswith('.mp3'):
        sound = AudioSegment.from_mp3(filePath)
        sound.export("{}.wav".format(os.path.splitext(filePath)[0]), format="wav")
    else:
        pass"""

    SAMPLE_RATE = 22050
    TRACK_DURATION = 30  # measured in seconds
    SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION

    FILE_DURATION = librosa.get_duration(filename=filePath)
    GET_FILE_DURATION = FILE_DURATION - 40
    RANDOM_OFFSET = random.randint(10, int(GET_FILE_DURATION))

    numSamplesPerSegment = int(SAMPLES_PER_TRACK / numSegments)
    expectedNumberMfccVectorsPerSegment = math.ceil(numSamplesPerSegment / hopLength)  # 1.2 => 2

    signal, sr = librosa.load(filePath, sr=SAMPLE_RATE, duration=30, offset=RANDOM_OFFSET)

    # process segments extracting mfcc and storing data
    for s in range(numSegments):
        start = numSamplesPerSegment * s  # s=0 => 0
        finish = start + numSamplesPerSegment  # s=0 => numSamplesPerSegment

        mfcc = librosa.feature.mfcc(signal[start:finish], sr=sr, n_fft=nFft, n_mfcc=nMfcc,
                                    hop_length=hopLength)

        mfcc = mfcc.T

        # store mfcc for segment if it has the expected length
        if len(mfcc) == expectedNumberMfccVectorsPerSegment:
            data["mfcc"].append(mfcc.tolist())

    with open(jsonPath, "w") as fp:
        json.dump(data, fp, indent=4)


def load_data(dataPath):
    with open(dataPath, "r") as fp:
        data = json.load(fp)

    # convert lists to numpy arrays
    mfcc = np.array(data["mfcc"])

    with open(dataPath, "w") as fp:
        pass

    return mfcc


def predict(file):
    FILE_PATH = f'/temp/media/{file}'

    save_mfcc(FILE_PATH, JSON_PATH, numSegments=10)
    X = load_data(JSON_PATH)

    # add a dimension to input data for sample - model.predict() expects a 4d array in this case
    X = X[..., np.newaxis]  # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = trainModel.predict(X)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)
    predicted_genre = genres.get(most_frequent(predicted_index))

    return predicted_genre
