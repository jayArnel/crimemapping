import matplotlib.pyplot as plt
import numpy as np
import os
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from django.conf import settings

from crimeprediction.vectorize import vectorize


if not hasattr(settings, 'OUTPUTS_DIR'):
    raise ImproperlyConfigured(
        'The directory to save output files is missing from your settings')
elif not os.path.exists(settings.OUTPUTS_DIR):
    os.makedirs(settings.OUTPUTS_DIR)


def run_network(grid_size, period, crime_type=None, seasonal=False):
    vectors = vectorize(
        grid_size, period, crime_type=crime_type, seasonal=seasonal)
    global_start_time = time.time()

    print 'Loading Data...'
    vectors = vectorize(grid_size, period)
    dim = len(vectors[0])
    result = np.array(vectors)

    print "Data  : ", result.shape

    row = int(round(0.7 * result.shape[0]))
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
    norm_predicted = predicted
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
                norm_predicted[x][y] = 1
                if node == 1:
                    correct += 1
                    truepos += 1
                else:
                    falsepos += 1
            else:
                norm_predicted[x][y] = -1
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

    crime_verbose = crime_type if crime_type is not None else "ALL"
    output_folder = settings.OUTPUTS_DIR + 'Results_{0}_{1}_{2}_{3}/'.format(
        grid_size, crime_verbose, period, seasonal)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results_file = output_folder + 'results.txt'
    predicted_file = output_folder + 'predicted.txt'
    accuracy_img = output_folder + 'accuracy.png'
    f1score_img = output_folder + 'f1score.png'

    np.savetxt(predicted_file, norm_predicted, fmt='%.6f')
    results = "Average Accuracy:" + str(np.average(accuracy)) + '\n'
    results += "Average F1 Score:" + str(np.average(f1scr))
    with open(results_file, "w") as output_file:
        output_file.write(results)

    if period == "daily":
        period_verbose = "Day"
    elif period == "weekly":
        period_verbose = "Week"
    elif period == "monthly":
        period_verbose = "Month"
    elif period == "yearly":
        period_verbose = "Year"

    # graph of Accuracy for each grid snapshot
    fig1 = plt.figure()
    plt.plot(accuracy)
    plt.xlabel(period_verbose)
    plt.ylabel('Accuracy')
    fig1.savefig(accuracy_img)
    # plt.show()

    # graph of F1 Score for each grid snapshot
    fig2 = plt.figure()
    plt.plot(f1scr)
    plt.xlabel(period_verbose)
    plt.ylabel('F1 Score')
    fig2.savefig(f1score_img)
    return model, y_test, predicted
