from flask import Flask, request
import json
import pandas as pd
import pickle
from utils.database import Database
from utils.process_input import validate_input


SAVED_MODEL_PATH = "files/classifier.pkl"
with open(SAVED_MODEL_PATH, "rb") as file:
    classifier = pickle.load(file)


database = Database()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home() -> tuple:
    """
    Homepage for this API.
    :return: Basic info about the API. A short introductory message
    """
    return ("""Welcome to Rafihatu Bello's item price prediction API. This API has only one useful endpoint \n
              Predict item prices based on ebay's prices."""), 200


@app.route("/predict", methods=["POST"])
def predict() -> json:
    """
    predicts the prices of items using the trained model based on the inputs passed in the request.
    :return: predicted price for the request
    """
    try:
        input_dataframe, transformed_data = validate_input(request.data)
        print(classifier.)
        prediction = classifier.predict(transformed_data)
        input_dataframe["outputs"] = prediction.tolist()
        database.add_prediction_result_to_database(input_dataframe)
        return json.dumps({"predicted_price(s)": prediction.tolist()}), 200
    except (KeyError, json.JSONDecodeError, AssertionError) as err:
        return json.dumps({"error": f"CHECK INPUT: {err}"}), 400
    except Exception as error:
        return json.dumps({"error": f"PREDICTION FAILED because {error}"}), 500



@app.route("/recent_predictions", methods=["GET"])
def recent_predictions():
    """
        fetches recently predicted details available in the database.
        :return: predicted price for the request
    """
    try:
        recent_ten = database.extract_predictions_from_database()
        return json.dumps({"recent_predictions": recent_ten})
    except Exception as error:
        return json.dumps({"error": f"REQUEST FAILED because {error}"}), 400


if __name__ == '__main__':
    app.run(debug=True)
