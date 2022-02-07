import json
import numpy as np
from keras import regularizers
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from tensorflow import keras
import matplotlib.pyplot as plt

DATA_PATH = "data.json"


def load_data(dataPath):
    with open(dataPath, "r") as fp:
        data = json.load(fp)

    # convert lists to numpy arrays
    mfcc = np.array(data["mfcc"])
    labels = np.array(data["labels"])

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


if __name__ == "__main__":
    # load data
    X, y = load_data(DATA_PATH)

    # split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # build the network
    model = Sequential([
        Flatten(input_shape=(X.shape[1], X.shape[2])),  # input layer, two dimensional array
        Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001)),  # 1st hidden layer
        Dropout(0.3),
        Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),  # 2nd hidden layer
        Dropout(0.3),
        Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),  # 3rd hidden layer
        Dropout(0.3),
        Dense(10, activation='softmax')  # output layer, 10 neurons = 10 genres
    ])

    # compile model
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # train model
    history = model.fit(X_train,
                        y_train,
                        epochs=100,
                        batch_size=32,
                        validation_data=(X_test, y_test))

    model.save('trainModel.h5', history)
    print('model created')

    # plot accuracy and error over epochs
    plot_history(history)
