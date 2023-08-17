# Important Modules
from flask import Flask, render_template, url_for, flash, redirect
# from forms import RegistrationForm, LoginForm
import joblib
from flask import request
import numpy as np
import tensorflow


import os
from flask import send_from_directory

import tensorflow as tf

app = Flask(__name__, template_folder='template')

# RELATED TO THE SQL DATABASE
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

import keras


dir_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

import tensorflow
from keras.models import load_model

global graph
graph = tf.get_default_graph()
model = load_model('malaria.h5')
model1 = load_model("pneumonia.h5")
model2 = tensorflow.keras.models.load_model("Covid_model.h5")

def api(full_path):
    with graph.as_default():
        data = keras.preprocessing.image.load_img(full_path, target_size=(50, 50, 3))
        data = np.expand_dims(data, axis=0)
        data = data * 1.0 / 255

        # with graph.as_default():
        predicted = model.predict(data)
        return predicted

# FOR THE SECOND MODEL
def api1(full_path):
    with graph.as_default():
        data = keras.preprocessing.image.load_img(full_path, target_size=(64, 64, 3))
        data = np.expand_dims(data, axis=0)
        data = data / 255

    # with graph.as_default():
        predicted = model1.predict(data)
        return predicted

def api111(full_path):
    with graph.as_default():
        data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
        data = np.expand_dims(data, axis=0)
        data = data / 255

    # with graph.as_default():
        predicted = model2.predict(data)
        return predicted




# procesing uploaded file and predict it
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    with graph.as_default():

        if request.method == 'GET':
            return render_template('malaria.html')
        else:
            #try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {0: 'PARASITIC', 1: 'Uninfected', 2: 'Invasive carcinomar', 3: 'Normal'}
            result = api(full_name)
            print(result)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            
            if accuracy<72:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"
            
            return render_template('malariapredict.html', image_file_name=file.filename, label=label, accuracy=accuracy, prediction = prediction)
        # except:
        #     flash("Please select the image first !!", "danger")
        #     return redirect(url_for("Malaria"))


@app.route('/upload11', methods=['POST', 'GET'])
def upload11_file():
    with graph.as_default():

        if request.method == 'GET':
            return render_template('pneumonia.html')
        else:
            #try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)
            indices = {0: 'Normal', 1: 'Pneumonia'}
            result = api1(full_name)
            if (result > 50):
                label = indices[1]
                accuracy = result
            else:
                label = indices[0]
                accuracy = 100 - result
            
            if accuracy<72:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"
                
            return render_template('pneumoniapredict.html', image_file_name=file.filename, label=label, accuracy=accuracy, prediction = prediction)
        # except:
        #     flash("Please select the image first !!", "danger")
        #     return redirect(url_for("Pneumonia"))



@app.route('/upload111', methods=['POST', 'GET'])
def upload111_file():
    with graph.as_default():

        if request.method == 'GET':
            return render_template('corona.html')
        else:
            #try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {1: 'Healthy', 0: 'Corona-Infected'}
            result = api(full_name)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            
            if accuracy<72:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"
                
            return render_template('coronapredict.html', image_file_name = file.filename, label = label, accuracy = accuracy, prediction = prediction)
        # except:
        #     flash("Please select the image first !!", "danger")
        #     return redirect(url_for("Pneumonia"))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/")
@app.route("/index1")
def index():
    return render_template("index1.html")

@app.route("/index2")
def index2():
    return render_template("index2.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/covid_19")
def covid_19():
    # if form.validate_on_submit():
    return render_template("corona.html")

@app.route("/Malaria")
def Malaria():
    return render_template("malaria.html")

@app.route("/Pneumonia")
def Pneumonia():
    return render_template("pneumonia.html"))

if __name__ == "__main__":
    app.run(debug=True)
