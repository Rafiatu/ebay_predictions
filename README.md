# Item Price Prediction API

## Description
This is a simple API that predicts item prices based on the `input` given in the post request.


## Getting Started

Using this API is very simple.
The API can be found on [Rafihatu's Heroku App](https://rafi-predict-prices.herokuapp.com/) and has just two useful endpoints: [predict](https://rafi-predict-prices.herokuapp.com/predict) 
and [recent_predictions](https://rafi-predict-prices.herokuapp.com/recent_predictions)

The predict endpoint takes only `POST` requests and request made to the endpoint should come with `input` as part of the request data.

The `input` should contain title and category of item whose price you want to predict. e.g 
```
import requests
import json


resp = requests.post("https://rafi-predictions.herokuapp.com/predict", 
                     data=json.dumps({"input":[{
                                                "title": "Black and white striped stockings",
                                                "category": "socks"
                                                },
                                                {
                                                "title": "Brand new Diamond sterling silver wrist bangle",
                                                "category": "bracelet"
                                                }
                                                ]
                                        }))
print(resp.text)
```
The API can also be tested using [Postman](https://www.postman.com) or [Swagger](https://swagger.io) like this
![Screenshot 2021-07-23 at 3 28 04 PM](https://user-images.githubusercontent.com/61936161/126781850-4c92e148-effa-4987-b4a0-25d06b2be3dd.png)


## License

The MIT License - Copyright (c) 2021 - Rafihatu Bello
