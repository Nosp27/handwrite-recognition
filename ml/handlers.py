import flask
from flask import request

from ml import model

app = flask.Flask(__name__)


@app.route("/predict")
def predict():
    return model.predict(request.json["image"])