from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D, Flatten, Activation, Dropout
from keras.models import Model, model_from_json
import numpy as np
import gzip
from keras.utils.data_utils import get_file
from keras.preprocessing import image
# from sklearn.utils import shuffle
# from sklearn.cross_validation import train_test_split
from keras import backend as K
from keras.utils import np_utils
from PIL import Image
import scipy.misc
import h5py
import os
from keras.utils.np_utils import to_categorical

class prettyfloat(float):
    def __repr__(self):
        return "%0.100f" % self

nb_channels = 3
nb_class = 5
kernel = 3
rows, cols = 128, 128
nb_epoch = 2
batch_size = 4

# labels[0:999] = 0 #cabbage
# labels[999:1999] = 1 #carrot
# labels[1999:2999] = 2 #cauliflower
# labels[2999:3999] = 3 #cucumber
# labels[3999:4999] = 4 #eggplant
# labels[4999:5999] = 5 #potato
# labels[5999:6999] = 6 #radish
# labels[6999:7999] = 7 #tomatto

import tensorflow as tf


def predict_from_model(images_to_predict):
    veg_name = {
        '0' : 'cabbage',
        '1' : 'carrot',
        '2' : 'cauliflower',
        '3' : 'cucumber',
        '4' : 'eggplant',
        '5' : 'potato',
        '6' : 'radish',
        '7' : 'tomatto',
    }
    with tf.Session():
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
        allpreds = model.predict(images_to_predict, batch_size=1)
        print(allpreds)

        # allpreds = allpreds.flatten()
        # map(prettyfloat, allpreds)

        veg_index = np.argmax(allpreds)
        print(veg_index)

        veg_name = veg_name[str(veg_index)]

        print(veg_name)

    return allpreds, veg_index, veg_name

K.clear_session()

# if '__main__':
#     f = image.load_img('./test/18.png', target_size=(128,128))
#     img = image.img_to_array(f)
#     print(predict_from_model(img))
    # import gc; gc.collect()
