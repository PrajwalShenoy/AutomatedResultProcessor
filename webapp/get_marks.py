from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = os.path.abspath('uploads')
DOWNLOADS_FOLDER = os.path.abspath('downloads')
ALLOWED_EXTENSIONS = {'txt'}
RESULT_URL = "https://www.dsce.edu.in/results"

class HelloWorld(Resource):
    def get(self):
        return {'Greeting': 'Hello There'}

class downloadResults(Resource):
    def post(self):
        try:
            files_uploaded = receive_upload(request)
            if files_uploaded[0]:
                return get_marks(files_uploaded[1])
            else:
                return {'error': 'File could not be uploaded'}
        except:
            return {'error': 'Something is wrong'}

def receive_upload(request):
    try:
        file = request.files['student_list']
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        return True, filename
    except:
        return False, 'false'

def allowed_filename(file_name):
    return file_name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def get_download_url():
    result_html = requests.get(RESULT_URL).content
    soup = BeautifulSoup(result_html, 'html.parser')
    for script in soup.find_all('script'):
        if "Please Enter USN" in str(script):
            download_link = str(script).split('url')[1].split("'")[1]
    return download_link

def get_marks(student_file):
    failed_downloads = []
    download_link = get_download_url()
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
            for student in student_list:
                result = requests.get(download_link + student.rstrip().upper())
                if result.status_code !=200:
                    failed_downloads.append(student.rstrip().upper())
                    continue
                with open(os.path.join(DOWNLOADS_FOLDER, student.rstrip().upper())+'.pdf', 'wb') as result_file:
                    result_file.write(result.content)
    return {'status': filename + ' saved successfully',
            'downloads': 'Complete',
            'failed_downloads': failed_downlods
            }

api.add_resource(HelloWorld, '/', '/hello')
api.add_resource(downloadResults, '/download-results')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)