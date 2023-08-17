from flask import Flask,render_template, url_for , redirect

from flask import request
import numpy as np



import os
import keras
import tensorflow as tf
import tensorflow
from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing import image

from flask import send_from_directory
# from keras.preprocessing import image
# import tensorflow as tf

#from this import SQLAlchemy
app=Flask(__name__,template_folder='template')



app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


dir_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
#from keras.models import load_model

global graph
graph = tf.get_default_graph()
model =load_model('Covid_model.h5')

# call model to predict an image
def api(full_path):
    with graph.as_default():

        data = tensorflow.keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
        #print(data.shape)
        data = np.expand_dims(data, axis=0)
        data = data/ 255

        #with graph.as_default():
        predicted = model.predict(data)
        return predicted


# procesing uploaded file and predict it
@app.route('/upload', methods=['POST','GET'])
def upload_file():
    with graph.as_default():

        if request.method == 'GET':
            return render_template('index.html')
        else:
            # try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {1: 'Healthy', 0: 'Corona-Infected'}
            result = api(full_name)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]

            return render_template('predict.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        # except :
        #     flash("Please select the image first !!", "danger")
        #     return redirect(url_for("corona"))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/")

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/corona")
def corona():
    return render_template("index.html")


if __name__ == "__main__":
	app.run(debug=True)
