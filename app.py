import os, cv2
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import tensorflow as tf
import keras
from keras_efficientnets import custom_objects

graph = tf.get_default_graph()
model = keras.models.load_model(
        "models/model_EfficientNetB3-opt.hdf5",
        custom_objects=custom_objects.get_custom_objects()
)

model.summary()

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        class_names = ["クラスA", "クラスB", "クラスC"]
        img_file = request.files['img_file']
        print(img_file.filename)
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(img_url)
            img = cv2.imread(img_url)
            in_img = np.expand_dims(img, axis=0) / 255.
            with graph.as_default():
                preds = model.predict_on_batch(in_img)[0]
            
            pred_cls = class_names[np.argmax(preds)]
            probs = [int(prob*100) for prob in list(preds)]
            payload = {
                "probs": probs, "pred_cls": pred_cls, "class_names": class_names}
            return payload
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
