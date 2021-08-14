import json
import pandas as pd
import pickle


with open("files/one_hot_encoder.pkl", "rb") as hot:
    one_hot_encoder = pickle.load(hot)


def process_input(dataframe: dict) -> tuple:
    data = pd.DataFrame(dataframe)
    transformed_data = one_hot_encoder.transform(data[['title', 'category']]).todense()
    return data, transformed_data


def validate_input(request_data: str) -> tuple:
    """
    asserts that the request data is correct.
    :param request_data: data gotten from the request made to the API
    :return: the processed dataframe of the request.data input
    """
    received = json.loads(request_data)["input"]
    assert type(received) == list and len(received) >= 1  # "'input' must be at least a dictionary with 2 parameters"
    data_to_be_predicted = {"title": [], "category": []}
    for item in range(len(received)):
        data_to_be_predicted["title"].append(received[item]["title"])
        data_to_be_predicted["category"].append(received[item]["category"])
    return process_input(data_to_be_predicted)
