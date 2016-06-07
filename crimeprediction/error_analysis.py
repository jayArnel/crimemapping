import matplotlib.pyplot as plt
import numpy as np

from sklearn.learning_curve import learning_curve
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasRegressor

from django.conf import settings

from crimeprediction.vectorize import vectorize


def build_model(dim, X):
    '''
    build function required by Scikit-Learn's learning curve function

    :param dim: dimension of the inputs
    :param X: data vector
    :rtype: contructed model
    '''
    print '\nData Loaded. Compiling...\n'
    model = Sequential()
    model.add(LSTM(dim, input_shape=X.shape[1:]))
    model.compile(loss='mse', optimizer='rmsprop',)
    return model


def plot_learning_curve(grid_size, period, crime_type=None, seasonal=False):
    '''
    Plots the learning curve using Scikit-Learn's learning_curve function,
        plots the graph using matplotlib and save sit

        :param grid_size: size of the cell dimension for the grid
        :param period: timestep of crime data
        :param crime_type: type of crime to be trained, None value will
            train all
        :param seasonal: implement seasonality or not
    '''
    vectors = vectorize(
        grid_size, period, crime_type=crime_type, seasonal=seasonal)

    print 'Loading Data...'
    dim = len(vectors[0])
    result = np.array(vectors)

    print "Data  : ", result.shape

    X = result[:-1]
    y = result[1:]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    estimator = KerasRegressor(

        build_fn=build_model, dim=dim, X=X, shuffle=False, nb_epoch=1000)
    fig1 = plt.figure()
    plt.title('Learning Curve')
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, verbose=10,
        train_sizes=(.1, 0.25, 0.5, 0.75, 1.0))
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std,
                     alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
    image_path = '{0}_{1}_{2}.png'.format(grid_size, period, seasonal)
    plt.legend(loc="best")
    fig1.savefig(image_path)
