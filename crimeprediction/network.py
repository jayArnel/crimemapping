import matplotlib.pyplot as plt
import numpy as np
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from crimeprediction.vectorize import vectorize


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
    model.add(LSTM(dim, input_shape=X_train.shape[1:]))
    model.compile(loss='mse', optimizer='rmsprop',)

    print("Train...")

    try:
        model.fit(X_train, y_train, nb_epoch=1000, shuffle=False)
    except KeyboardInterrupt:
        pass

    print 'Training duration (s) : ', time.time() - global_start_time
    predicted = model.predict(X_test)

    accuracy = []
    f1scr = []

    for x, data in enumerate(y_test):
        print len(data)
        print len(predicted[x])
        correct = 0
        total = 0
        truepos = 0
        falsepos = 0
        trueneg = 0
        falseneg = 0

        for y, node in enumerate(data):
            total += 1
            if predicted[x][y] > 0:  # threshold for prediction. If prediction is greater than this value, prediction is one, zero otherwise
                if node == 1:
                    correct += 1
                    truepos += 1
                else:
                    falsepos += 1
            else:
                if node == -1:
                    correct += 1
                    trueneg += 1
                else:
                    falseneg += 1
        print "correct", correct
        print "total", total
        act = float(correct) / total
        print act
        accuracy.append(act)

        precision = truepos / float(truepos+falsepos)
        recall = truepos / float(truepos+falseneg)

        f1 = (precision * recall * 2) / float(precision + recall)

        f1scr.append(f1)

        print accuracy
        print f1

    print "Average Accuracy:", np.average(accuracy)
    print "Average F1 Score:", np.average(f1scr)

    # graph of Accuracy for each grid snapshot
    fig1 = plt.figure()
    plt.plot(accuracy)
    plt.xlabel('Week')
    plt.ylabel('Accuracy')
    fig1.savefig("Accuracy.png")
    # plt.show()

    # graph of F1 Score for each grid snapshot
    fig2 = plt.figure()
    plt.plot(f1scr)
    plt.xlabel('Week')
    plt.ylabel('F1 Score')
    fig2.savefig("F1Score.png")
    return model, y_test, predicted
