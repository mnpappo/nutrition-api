from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D, Flatten, Activation, Dropout
from keras.models import Model, model_from_json
import numpy as np
import gzip
from keras.utils.data_utils import get_file

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from keras import backend as K
from keras.utils import np_utils
from PIL import Image
import scipy.misc
import h5py
import os
from keras.utils.np_utils import to_categorical

class prettyfloat(float):
    def __repr__(self):
        return "%0.10f" % self

nb_channels = 3
nb_class = 5
kernel = 3
rows, cols = 64, 64
nb_epoch = 2
batch_size = 4


def predict_from_model(images_to_predict):
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_json_path = 'model.json'
    model_weight_path = 'weight.h5'

    json_file = open(BASE_PATH + '/api/' + model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    model = model_from_json(loaded_model_json)

    model.load_weights(BASE_PATH + '/api/' + model_weight_path)

    # model.evaluate(x_test, y_test, verbose=1)

    images_to_predict = images_to_predict.reshape(1, nb_channels, rows, cols)

    print("Predicting......")
    preds = model.predict(images_to_predict, batch_size=1)
    preds = preds.flatten()

    print(preds)

    x = map(prettyfloat, preds)

    return x