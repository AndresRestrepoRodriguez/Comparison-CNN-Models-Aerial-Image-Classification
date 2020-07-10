import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.models import load_model



def initialize_model():
    model = Sequential()
    return model

def add_conv2d_initial(filters, padding, kernel_size, activation, model):
    filters = int(filters)
    kernel = int(kernel_size)
    model.add(Conv2D(filters, (kernel, kernel),input_shape=(224, 224, 3), padding=padding, activation=activation))
    #print(model.summary())
    print('convI')

def add_conv2d(filters, padding,kernel_size, activation, model):
    filters=int(filters)
    kernel = int(kernel_size)
    model.add(Conv2D(filters, (kernel, kernel), padding=padding, activation=activation))
    #print(model.summary())
    print('conv')

def add_maxPooling2d(size_a, size_b, padding, model):
    size_pool_a = int(size_a)
    size_pool_b = int(size_b)
    model.add(MaxPooling2D(pool_size=(size_pool_a, size_pool_b), padding=padding))
    #print(model.summary())
    print('max')

def add_dropout(rate, model):
    rate=float(rate)
    model.add(Dropout(rate))
    #print(model.summary())
    print('drop')

def add_dense(units, activation, model):
    units=int(units)
    model.add(Dense(units, activation=activation))
    #print(model.summary())
    print('dense')

def add_flatten(model):
    model.add(Flatten())
    #print(model.summary())
    print('flatten')

def conv_string_to_array(cadena):
    array_hyperparameters=cadena.split(",")
    return array_hyperparameters


def generate_model(array_layers_data, model, nClasses):
    model_local = model
    temporal_data = []
    cont_conv2d = 0
    for i in range(len(array_layers_data)):
        temporal_data = conv_string_to_array(array_layers_data[i])
        layer_kind = temporal_data[0]
        if(layer_kind == 'conv2d'):
            if(cont_conv2d > 0):
                add_conv2d(temporal_data[1],temporal_data[2],temporal_data[3],temporal_data[4],model_local)
            else:
                add_conv2d_initial(temporal_data[1],temporal_data[2],temporal_data[3],temporal_data[4],model_local)
            cont_conv2d = cont_conv2d + 1
        elif(layer_kind == 'maxpooling2d'):
            add_maxPooling2d(temporal_data[1],temporal_data[2],temporal_data[3], model_local)
        elif(layer_kind == 'dropout'):
            add_dropout(temporal_data[1], model_local)
        elif(layer_kind == 'dense'):
            add_dense(temporal_data[1], temporal_data[2], model_local)
        else:
            add_flatten(model_local)
    model_local.add(Dense(nClasses, activation='softmax'))
    return model_local

def compilation_model(optimizer, loss_function, metric, model):
    model.compile(optimizer=optimizer, loss=loss_function, metrics=[metric])
    model.summary()
    return model

def fit_model(model, train_data, train_target, epochs, batch_size):
    epochs = int(epochs)
    batch_size = int(batch_size)
    history = model.fit(train_data, train_target, epochs=epochs, batch_size=batch_size, verbose=1)
    #model.save('/home/ubuntu/deeplearningsateliteimagery/models/model.h5')
    return model

def evaluate_model(model, test_data, test_target):
    model_local_evaluate = model.evaluate(test_data, test_target)
    return model_local_evaluate[0], model_local_evaluate[1]
