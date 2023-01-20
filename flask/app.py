from bson.json_util import dumps
from flask import Flask, request, make_response
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://mymongo:27017/myDB"
mongo = PyMongo(app)


class User(Resource):

    def get(self):
        user_list = []
        user_data = mongo.db.users
        for user in user_data.find():
            user_list.append(user)
        return dumps(user_list)

    def post(self):
        if request.is_json:
            try:
                data = request.get_json()
                name = data['name']
                email = data['email']
                user_id = data['user_id']

                if user_id not in [i['user_id'] for i in mongo.db.users.find()]:
                    mongo.db.users.insert_one({"name": name, "email": email, "user_id": user_id})
                    return make_response({"message": "user added successfully"}, 201)
                else:
                    return make_response({"message":f"user with id {user_id} already exist please another id"},400)

                
            except KeyError:
                return make_response({"message": "invalid json format",
                                      "valid format": {"name": "your_name",
                                                       "email": "your_email",
                                                       "user_id": "id"}}, 400)


class One_User(Resource):

    def get(self):
        if request.is_json:
            try:
                user = request.get_json()
                u_id = user['user_id']
                if u_id in [i['user_id'] for i in mongo.db.users.find()]:
                    user = mongo.db.users.find_one({"user_id": u_id})
                    return dumps(user)
                else:
                    return make_response({"message": "Enter valid 'user_id' "}, 404)

            except KeyError:
                return make_response({"message": "invalid json format", "valid_format": {"user_id": "id"}}, 400)

    def put(self):
        if request.is_json:
            try:
                data = request.get_json()

                myquery = {"user_id": data['user_id']}
                values = {"$set": {"email": data['email'], "name": data['name']}}

                mongo.db.users.update_one(myquery, values)

                return make_response({"message": "user updated successfully"}, 201)

            except KeyError:
                return make_response({"message": "invalid json format", "valid_format": {"user_id": "id",
                                                                                         "name": "your_name",
                                                                                         "email": "your_email"
                                                                                         }}, 400)

    def delete(self):
        if request.is_json:
            try:
                data = request.get_json()
                user_id = data['user_id']
                # user_ids = []
                # for user in mongo.db.users.find():
                #     user_ids.append(user['user_id'])
                if user_id in [i['user_id'] for i in mongo.db.users.find()]:
                    mongo.db.users.delete_one({"user_id": user_id})
                    return make_response({"message": f'user with id {user_id} deleted !!!'}, 200)
                else:
                    return make_response({"message": "enter valid 'user_id'"}, 404)

            except KeyError:
                return make_response({"message": "invalid json format", "valid_format": {"user_id": "id"}}, 400)


class NonDB(Resource):
    def get(self):
        return "Hello"


api.add_resource(User, '/api/user')
api.add_resource(One_User, '/api/one')
api.add_resource(NonDB,'/non')