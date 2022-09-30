from crypt import methods
from urllib import request
from flask import Blueprint, jsonify, request, Response, make_response
from pymongo import MongoClient
import certifi
from bson import json_util
from datetime import datetime

querys = Blueprint("querys", __name__)
uri = "mongodb+srv://ivanwekis:MmongodbB@cluster0.srdnijs.mongodb.net/test"
ca = certifi.where()
client = MongoClient(uri, tlsCAFile=ca)
dbnasdaq = client["nasdaq"]
dbusers = client["nasdaq-users"]

def info_stock(stock):
    username = request.cookies.get("username-id")
    print(stock)
    print(username)
    if not username is None:
        stock_data = dbnasdaq.get_collection(stock)
        data = json_util.dumps(stock_data.find())
        response = make_response(Response(data, mimetype="application/json"))
        response.set_cookie("username-id", username)
        return response
    else:
        return jsonify({"response": "You should be logged first"})
    


def info_stock_date(stock, date):
    username = request.cookies.get("username-id")
    try:
        datetime.strptime(date, "%m-%d-%Y")
        list = date.split("-")
        date_query = str(list[0]) +"/"+ str(list[1])+"/"+str(list[2])
    except ValueError as exception:
        return jsonify(
            {
                "response": "The date format is invalid. %m-%d-%Y",
                "exception": str(exception),
            }
        )

    if not username is None:
        stock_data = dbnasdaq.get_collection(stock)
        data = json_util.dumps(stock_data.find({"Date": date_query}))
        response = make_response(Response(data, mimetype="application/json"))
        response.set_cookie("username-id", username)
        return response

    else:
        return jsonify({"response": "You should be logged first"})
    


@querys.errorhandler(404)
def not_found():
    return jsonify({"response": "Invalid route"})