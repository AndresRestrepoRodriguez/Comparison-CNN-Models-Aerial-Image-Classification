import numpy as np
import pickle
from pathlib import Path
import h5py
from skimage import io, transform
import os
from keras.utils import np_utils

folders = ['airplane','airport','commercial_area','forest', 'freeway','island','ship','stadium']

path_base = "/folder/"

def load_test_images():
    x_test = np.empty((1239, 224, 224, 3), dtype='float32')
    lista_images = []
    for i in range(len(folders)):
        list_a = os.listdir(path_base+"dataset/test/"+folders[i]) # dir is your directory path
        number_files = len(list_a)
        print(folders[i])
        for j in range(1,number_files+1):
            test_image = io.imread(path_base+"dataset/test/"+folders[i]+"/"+str(j)+'.jpg')
            test_image = transform.resize(test_image,(224,224))
            test_image = np.asarray(test_image).astype(np.float32)
            lista_images.append(test_image)
    for i in range(len(lista_images)):
        x_test[i] = lista_images[i]
    return x_test

def load_test_targets():
    lista_labels = []
    for i in range(len(folders)):
        list_a = os.listdir(path_base+"dataset/test/"+folders[i]) # dir is your directory path
        number_files = len(list_a)
        print(folders[i])
        for j in range(number_files):
            lista_labels.append(i)
    y_test = np.array(lista_labels)
    return y_test



def process_data(x_test, y_test, num_classes):
    nRows,nCols,nDims = x_test.shape[1:]
    test_data = x_test.reshape(x_test.shape[0], nRows, nCols, nDims)
    test_data = test_data.astype('float32')
    test_target = y_test.reshape(y_test.shape[0],1)
    test_target = np_utils.to_categorical(test_target.astype(np.int64), num_classes)
    return  test_data, test_target
