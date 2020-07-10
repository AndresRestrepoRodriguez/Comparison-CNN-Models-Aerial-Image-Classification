import keras
from keras.models import load_model
from keras import backend as K



def load_model_cnn(ruta):
    print('entre load vry')
    K.clear_session()
    model = load_model(ruta)
    return model

def verify_layers(model):
    array_layers = model.layers
    length_layers = len(array_layers)
    count = 0
    val_conv = True
    val_last_layer = True
    val_input_shape = True
    if(array_layers[length_layers-1].units != 8):
        val_last_layer = False

    return val_last_layer

"""
def verify_model(ruta):
    val_model_load = True
    try:
        model = load_model_cnn(ruta)
    except:
        val_model_load = False
    if (val_model_load == True):
        val_conv, val_last_layer, val_input_shape = verify_layers(model)
        if(val_conv == False):
            return [False, 'Your model does not have a Convolutional Layers']
        elif(val_last_layer == False):
            return [False, 'Your model does not have 8 classes as output layer']
        elif(val_input_shape == False):
            return [False, 'Your model does not have a input shape (224,224,3)']
    else:
        return [False, 'Your model is not a CNN']

    return [True, 'Good Model']
"""

def verify_model(ruta):
    val_model_load = True
    try:
        model = load_model_cnn(ruta)
    except:
        val_model_load = False
    if(val_model_load == False):
        return [False, 'Problems loading the model']
    else:
        val_last = verify_layers(model)
        if(val_last == False):
            return [False, 'Problems loading the model. More classes than expected']
        else:
            return [True, 'Good Model']
