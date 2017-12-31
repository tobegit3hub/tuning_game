from __future__ import print_function

import json

import keras
from keras.datasets import mnist
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import RMSprop

from abstract_competition import AbstractCompetition


class MnistKerasDnn(AbstractCompetition):
  """
  Deep neural network model in Keras.
  """

  def execute(self, parameters_instance):

    # Example: {"batch_size": 128, "hidden1": 512, "hidden2": 512}
    parameters_json = json.loads(parameters_instance)
    batch_size = parameters_json["batch_size"]
    hidden1 = parameters_json["hidden1_number"]
    hidden2 = parameters_json["hidden2_number"]

    metrics = self.train(batch_size, hidden1, hidden2)

    return metrics

  def train(self, batch_size=128, hidden1=512, hidden2=512):
    num_classes = 10
    #epochs = 20
    epochs = 1

    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Dense(hidden1, activation='relu', input_shape=(784, )))
    model.add(Dropout(0.2))
    model.add(Dense(hidden2, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(
        loss='categorical_crossentropy',
        optimizer=RMSprop(),
        metrics=['accuracy'])

    history = model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        verbose=1,
        validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    return score[1]
