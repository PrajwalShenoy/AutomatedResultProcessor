from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# todos = {}

# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {todo_id: todos[todo_id]}

#     def post(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}

UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = {'txt'}

class uploadFile(Resource):
    def post(self):
        print('.............--.......')
        try:
            file = request.files['student_list']
            print('.')
            if file and allowed_filename(file.filename):
                print('..')
                filename = secure_filename(file.filename)
                print('...')
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                print('....')
                return {'status': filename + ' saved successfully'}
        except:
            return {'error': 'Something is wrong'}

def allowed_filename(file_name):
    return file_name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



api.add_resource(HelloWorld, '/', '/hello')
# api.add_resource(TodoSimple, '/<int:todo_id>')
api.add_resource(uploadFile, '/upload')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)