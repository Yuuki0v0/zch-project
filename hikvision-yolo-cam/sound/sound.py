#### Extracting MFCC's For every audio file
import pandas as pd
import os
import librosa
import time
#import pyaudio
import numpy as np
from tqdm import tqdm

from tensorflow.keras.utils import to_categorical
#from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation,Flatten
from tensorflow.keras.optimizers import Adam
from sklearn import metrics
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime

from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import load_model
import keras

split_fold_num = 9


def load_model_1(file_path):
    return keras.models.load_model(file_path, compile=False)


def model_load(file):
    global model
    print("============== MODEL LOAD ==============")
    model_file = file
    print('model_file:', model_file)
    try:
        model = load_model_1(model_file)
    except:
        model = load_model(model_file)
    model.summary()
    return model


# model = load_model('saved_models/final_model.hdf5')
# labelencoder=LabelEncoder()
def model_pred(filename):
    global model
    start_time = time.time()

    # filename = "/home/u20/PycharmProjects/PROJECT/motor_sound/sound_recognition/dev_data/data/20220328_111007851_90_11111.wav"
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)

    # print(mfccs_scaled_features)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    # print(mfccs_scaled_features.shape)
    # print(mfccs_scaled_features.shape)
    predicted_label = np.argmax(model.predict(mfccs_scaled_features), axis=1)
    # prediction_class = labelencoder.inverse_transform(predicted_label)

    end_time = time.time()
    print('预测结果', predicted_label)
    # print(prediction_class)
    total_time = end_time - start_time
    return predicted_label, total_time

