from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

messages = {}

class ChatServer(Resource):
    def get(self):
        return messages
    def put(self, author):
        messages[author] = request.form['content']
        return {author: messages[author]}

api.add_resource(ChatServer, '/<string:author>', '/buddy')
if __name__ == '__main__':
    app.run(debug=True)
