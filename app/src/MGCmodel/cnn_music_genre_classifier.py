import json
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow import keras
import matplotlib.pyplot as plt

# preprocessed data
DATA_PATH = "data.json"


def load_data(dataPath):
    with open(dataPath, "r") as fp:
        data = json.load(fp)

    # convert lists to numpy arrays
    mfcc = np.array(data["mfcc"])  # inputs
    labels = np.array(data["labels"])  # outputs

    print("Data successfully loaded!")

    return mfcc, labels


def plot_history(his):
    fig, axs = plt.subplots(2)

    # create accuracy subplot
    axs[0].plot(his.history["accuracy"], label="train accuracy")
    axs[0].plot(his.history["val_accuracy"], label="test accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy eval")

    # create error subplot
    axs[1].plot(his.history["loss"], label="train error")
    axs[1].plot(his.history["val_loss"], label="test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error eval")

    plt.show()


def prepare_datasets(testSize, validationSize):
    # load data
    X, y = load_data(DATA_PATH)

    # create train and validation split
    XTrain, XTest, YTrain, YTest = train_test_split(X, y, test_size=testSize)
    XTrain, XValidation, YTrain, YValidation = train_test_split(XTrain, YTrain, test_size=validationSize)

    # 3d array for each sample
    XTrain = XTrain[..., np.newaxis]  # 4d array
    XValidation = XValidation[..., np.newaxis]
    XTest = XTest[..., np.newaxis]

    return XTrain, XValidation, XTest, YTrain, YValidation, YTest


def build_model(inputShape):
    # build the network
    model = Sequential([
        # 1st conv layer
        Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=inputShape),
        MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same'),
        BatchNormalization(),
        # 2nd conv layer
        Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same'),
        BatchNormalization(),
        # 3rd conv layer
        Conv2D(filters=32, kernel_size=(2, 2), activation='relu'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
        BatchNormalization(),
        # flatten output and feed it into dense layer
        Flatten(),
        Dense(units=64, activation='relu'),
        Dropout(0.1),
        # output layer
        Dense(units=10, activation='softmax')
    ])

    return model


def predict_test(model, X, y):
    # add a dimension to input data for sample - model.predict() expects a 4d array in this case
    X = X[np.newaxis, ...]  # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = model.predict(X)

    # get index with max value
    predictedIndex = np.argmax(prediction, axis=1)

    print(f"Target: {y}, Predicted label: {predictedIndex}")


if __name__ == "__main__":
    # get train, validation, test splits
    xTrain, xValidation, xTest, yTrain, yValidation, yTest = prepare_datasets(0.25, 0.2)

    # create network
    trainModel = build_model((xTrain.shape[1], xTrain.shape[2], 1))

    # compile model
    trainModel.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])

    trainModel.summary()

    # train model
    history = trainModel.fit(
        xTrain,
        yTrain,
        validation_data=(xValidation, yValidation),
        batch_size=32,
        epochs=30)

    # plot accuracy and error over epochs
    plot_history(history)

    # evaluate model on test set
    testLoss, testAcc = trainModel.evaluate(xTest, yTest, verbose=2)
    print('\nTest accuracy:', testAcc)

    trainModel.save('trainModel.h5', history)
    print('model created')

    trainModel = load_model('trainModel.h5')

    # pick a sample to predict from the test set
    xToPredict = xTest[100]
    yToPredict = yTest[100]

    # predict sample
    predict_test(trainModel, xToPredict, yToPredict)
