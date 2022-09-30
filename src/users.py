from types import NoneType
from pymongo import MongoClient
import certifi
from flask import request, make_response,jsonify
from werkzeug.security import check_password_hash, generate_password_hash

uri = "mongodb+srv://ivanwekis:MmongodbB@cluster0.srdnijs.mongodb.net/test"
ca = certifi.where()
client = MongoClient(uri, tlsCAFile=ca)
db = client["nasdaq-users"]


def new_user():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        rpassword = request.json["rpassword"]
    except KeyError as error:
        return jsonify({"response": "The data isn`t correct", "error": str(error)})

    if password == rpassword:
        query = {"username": username}
        query2 = {"email": email}
        if db.users.find_one(query) is None:
            if db.users.find_one(query2) is None:
                hashed_password = generate_password_hash(password)
                new_user = {
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                }
                db.users.insert_one(new_user)
                return jsonify({"response": "The new user has been added"})
            else:
                return jsonify({"response": "Alredy exists an account with that email"})

        else:
            return jsonify({"response": "Alredy exists that username"})

    else:
        return jsonify({"response": "Please check the passwords"})

        
def login():
    username = request.json["username"]
    password = request.json["password"]
    try:
        user = db.users.find_one({"username": username})
        hashed_password = user["password"]
        if check_password_hash(hashed_password, password):
            cookie = make_response({"response": "Login succesfully"})
            cookie.set_cookie("username-id", username, max_age=300)
            return cookie
        else:
            return jsonify({"response": "The username or password are invalid "})
    except TypeError:
        return jsonify({"response": "The username or password are invalid"}) 