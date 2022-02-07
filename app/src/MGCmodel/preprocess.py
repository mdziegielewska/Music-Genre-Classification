import json
import os
import librosa
import math

DATASET_PATH = "trainData"  # https://www.kaggle.com/andradaolteanu/gtzan-dataset-music-genre-classification
JSON_PATH = "data.json"

SAMPLE_RATE = 22050
TRACK_DURATION = 30  # measured in seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION


# nMfcc - number of coefficients to extract
# nFft - interval we consider to apply FFT, measured in number of samples
# hopLength - sliding window for FFT, measured in number of samples
# numSegments - number of segments we want to divide sample tracks into
def save_mfcc(datasetPath, jsonPath, nMfcc=13, nFft=2048, hopLength=512, numSegments=5):
    # dictionary to store data
    data = {
        "mapping": [],  # genres
        "mfcc": [],  # inputs
        "labels": []  # outputs
    }

    numSamplesPerSegment = int(SAMPLES_PER_TRACK / numSegments)
    expectedNumberMfccVectorsPerSegment = math.ceil(numSamplesPerSegment / hopLength)  # 1.2 => 2

    # loop through all the genres
    for i, (dirPath, dirNames, filenames) in enumerate(os.walk(datasetPath)):
        # ensure that we are not at the root level
        if dirPath == datasetPath:
            pass
        else:
            # save the semantic label
            dirPathComponents = dirPath.split("\\")  # genre/blues => ["genre", "blues"]
            semanticLabel = dirPathComponents[-1]  # takes the last element
            print(semanticLabel)
            data["mapping"].append(semanticLabel)
            print("\nProcessing {}".format(semanticLabel))

            # process files for a specific genre
            for f in filenames:
                # load audio file
                filePath = os.path.join(dirPath, f)
                signal, sr = librosa.load(filePath, sr=SAMPLE_RATE)

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
                        data["labels"].append(i-1)

                        print("{}, segment:{}".format(filePath, s+1))

    with open(jsonPath, "w") as fp:
        json.dump(data, fp, indent=4)

    print("Data extracted")


if __name__ == "__main__":
    save_mfcc(DATASET_PATH, JSON_PATH, numSegments=10)
