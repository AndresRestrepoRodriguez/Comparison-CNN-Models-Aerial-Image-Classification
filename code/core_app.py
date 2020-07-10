from flask import Flask, render_template, request, jsonify
import numpy as np
import verify_model as vm
import Data_processing as dp
import metrics as m
import pdf_generator as pg
import email_controler as ec
import os
#import magic
import urllib.request
#from app import app
from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/folder/code/static/own_model'

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'h5'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
	return render_template('principal.html')

@app.route('/manuales')
def manuales():
	return render_template('manuales.html')

@app.route('/uploadajax', methods=['POST'])
def model():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'model.h5'))
    ruta_model = UPLOAD_FOLDER+'/model.h5'

    result_model = vm.verify_model(ruta_model)

    if (result_model[0]) :
        return jsonify({ 'success' :  'Model verified successfully' })
    else:
        return jsonify({'error' : result_model[1]})



@app.route('/comparar', methods=['POST'])
def process():

    data = request.form

    data_dictionary = data.copy()
    print(data_dictionary)
    final_models= []

    model_option = data_dictionary["model_option"]
    pretrained_models = data_dictionary["pretrained_models"].split(",")
    if(model_option == 'yes'):
        model_file = data_dictionary["model_file"]
        final_models = pretrained_models
        final_models.append('own_model')
    else:
        final_models = pretrained_models
    email_user = data_dictionary["email_user"]

    #print('final_models')
    #print(model_file)

    if(model_option == 'yes'):
	#Verify model
        print('empece a leer')
        model = vm.load_model_cnn(model_file)
        print('acabe a leer')
	    #Processing Images
        x_test = dp.load_test_images()
        y_test = dp.load_test_targets()
        test_data, test_target = dp.process_data(x_test, y_test, 8)

	    #Generate metrics
        m.generate_metrics(model, test_data, test_target, y_test, x_test)

    #Generate pdf
    fpr_micro, tpr_micro, fpr_macro, tpr_macro = pg.load_metrics_data_roc(final_models)
    report_values = pg.load_metrics_data_report(final_models)
    ruta_macro = pg.generate_graphs_macro(final_models, fpr_macro, tpr_macro)
    ruta_micro = pg.generate_graphs_micro(final_models, fpr_micro, tpr_micro)
    pg.generate_pdf(ruta_micro, ruta_macro, report_values)

	#Send Email
    #ec.zip(directory_results,name_destination)
    ec.send_results(email_user)






    if (data_dictionary) :
        return jsonify({ 'success' :  'Successfully Process Please Ckeck your Email' })
    else:
        parametros=[]
        return jsonify({'error' : 'Problemas with the process. Try Again'})








if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port='28600')
