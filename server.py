from flask import Flask, request, Response
from bson.json_util import dumps
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "URL_MONGODB"
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def getUsers():
    usersDB = mongo.db.users.find({})

    usersList = list(usersDB)

    json_users = dumps(usersList)

    return json_users


@app.route('/', methods=['POST'])
def createUser():
    username = request.json['username']
    password = request.json['password']

    if username and password:
        _id = mongo.db.users.insert_one({
            'username': username, 
            'password': password
        })

        response = {
            'id': str(_id.inserted_id),
            'username': username, 
            'password': password
        }

        return response
    else:
        return {'error': 'Invalid username or password'}



if __name__ == '__main__':
    app.run(debug=True)
