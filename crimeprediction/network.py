import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import sys
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from crimeprediction.vectorize import vectorize
sys.setrecursionlimit(10000)

np.random.seed(1234)


def crime_data(grid_size=1000, period='yearly'):
    vectors = vectorize(grid_size, period)
    dim = len(vectors[0])
    result = np.array(vectors)

    print "Data  : ", result.shape

    row = round(0.9 * result.shape[0])
    train = result[:row, :]
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = result[row:, :-1]
    y_test = result[row:, -1]

    return [X_train, y_train, X_test, y_test, dim]


# def build_model(dim):
#     model = Sequential()
#     layers = [1, dim, dim * 2, 1]

#     model.add(LSTM(
#         input_dim=layers[0],
#         output_dim=layers[1],
#         return_sequences=True))
#     model.add(Dropout(0.2))

#     model.add(LSTM(
#         layers[2],
#         return_sequences=False))
#     model.add(Dropout(0.2))

#     model.add(Dense(
#         output_dim=layers[3]))
#     model.add(Activation("linear"))

#     start = time.time()
#     model.compile(loss="mse", optimizer="rmsprop")
#     print "Compilation Time : ", time.time() - start
#     return model


def run_network(grid_size=1000, period='yearly'):
    vectors = vectorize(grid_size, period)
    global_start_time = time.time()
    epochs = 1
    ratio = 0.5
    sequence_length = 50
    path_to_dataset = 'household_power_consumption.txt'

    print 'Loading Data...'
    vectors = vectorize(grid_size, period)
    dim = len(vectors[0])
    result = np.array(vectors)

    print "Data  : ", result.shape

    row = round(0.5 * result.shape[0])
    train = result[:row]
    X_train = train[:-1]
    y_train = train[1:]
    test = result[row:]
    X_test = test[:-1]
    y_test = test[1:]

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    print '\nData Loaded. Compiling...\n'
    print X_train
    print y_train
    model = Sequential()
    model.add(LSTM(
        dim, input_shape=X_train.shape[1:]))
    model.compile(loss='mse', optimizer='rmsprop',)

    print("Train...")
    model.fit(X_train, y_train, nb_epoch=3, shuffle=False)
    # score, acc = model.evaluate(X_test, y_test,
    #                             show_accuracy=True)

    # try:
    #     model.fit(
    #         X_train, y_train,
    #         batch_size=512, nb_epoch=epochs, validation_split=0.05)
    predicted = model.predict(X_test)
    # except KeyboardInterrupt:
    #     print 'Training duration (s) : ', time.time() - global_start_time
    #     return model, y_test, 0

    try:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(y_test[:100, 0])
        plt.plot(predicted[:100, 0])
        plt.show()
    except Exception as e:
        print str(e)
    print 'Training duration (s) : ', time.time() - global_start_time
    print len(y_test[0])
    print len(predicted[0])
    return model, y_test, predicted
