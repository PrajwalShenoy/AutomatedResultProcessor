from flask import Flask, request, send_file, render_template, make_response
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from get_marks import receive_upload, allowed_filename
from get_marks import UPLOAD_FOLDER, DOWNLOADS_FOLDER, ALLOWED_EXTENSIONS
import pandas as pd
import os
import requests
import PyPDF2
import re

REPORTS_FOLDER = os.path.abspath('reports')

app = Flask(__name__)
api = Api(app)

reg_ex = {0: "[1-9]{2}[A-Z]{2}[0-9][A-Z]{5}",
          1: "[A-Z]{2,3}[1-9]{2}",
          2: "[1-9]{2}[A-Z]{3,5}[1-9]{2,3}",
          3: "[A-Z]{6}[0-9]{2,3}",
          4: "[1-9]{2}[A-Z]{2}[0-9][A-Z]{4,5}[0-9]{0,1}"}

headers = {'Content-Type': 'text/html'}
html_page = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=student_list>
      <input type=submit value=Upload>
    </form>
    '''

class ProcessMarks(Resource):
    def post(self):
        try:
            files_uploaded = receive_upload(request)
            if files_uploaded[0]:
                if verify_downloads(files_uploaded[1]):
                    df = process_marks(files_uploaded[1])
                    process_df(df, files_uploaded[1])
                    return send_file(os.path.join(REPORTS_FOLDER, files_uploaded[1][:-3]+'.csv'))
                else:
                    return {'error': 'Some files are not present, please re-download them'}
            else:
                return {'error': 'File could not be uploaded'}
        except:
            return {'error': 'Something is wrong'}
    
    def get(self):
        return make_response(html_page,200,headers)

def process_df(df, file_name):
    df.to_csv(os.path.join(REPORTS_FOLDER, file_name[:-3]+'.csv'))

def verify_downloads(student_file):
    file_list = os.listdir('downloads')
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
        for student in student_list:
            if student.rstrip() + '.pdf' not in  file_list:
                return False
    return True

def process_marks(student_file):
    df = pd.DataFrame()
    df['Name'] = None
    df['SGPA'] = None
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
        for student in student_list:
            try:
                pdf = PyPDF2.PdfFileReader(os.path.join(DOWNLOADS_FOLDER, student.rstrip()+'.pdf'))
                num_of_pages = pdf.getNumPages()
                for pg_num in range(num_of_pages):  
                    print(student, end='')
                    df = process_page(pdf, pg_num, df, student.rstrip())
            except:
                print("Could not process", student)
    return df

def process_page(pdf, pg_num, df, student):
    pdf_text = pdf.getPage(pg_num).extractText()
    df.loc[student, 'Name'] = re.search("(?<=Student:).*USN", pdf_text).group()[:-3]
    match = re.search("(?<=GRADE POINTS1).*Letter Grades", pdf_text)
    reduced_text = pdf_text[match.span()[0]:match.span()[1]]
    split_match = re.split(select_regex(reduced_text), reduced_text)[1:]
    split_match[-1], sgpa = split_match[-1].split('SGPA')
    df.loc[student, 'SGPA'] = sgpa.split('L')[0]
    split_match = [subject[:-1] for subject in split_match[:-1]] + [split_match[-1]]
    split_match = [re.split("[0-9]{1}[A-Z]{1,2}[+]{0,1}", subject) for subject in split_match]
    df = check_for_sub_heading(split_match, df)
    df = update_marks(split_match, df, student)
    print(split_match)
    print()
    return df

def select_regex(reduced_text):
    lens = []
    for key, val in reg_ex.items():
        lens.append(len(re.split(val, reduced_text)[1:]))
    return reg_ex[lens.index(max(lens))]

def check_for_sub_heading(split_match, df):
    heading = [split[0] for split in split_match]
    for sub in heading:
        if sub not in list(df.columns):
            df[sub] = None
    return df

def update_marks(split_match, df, student):
    for subject in split_match:
        df.loc[student, subject[0]] = subject[1]
    return df

api.add_resource(ProcessMarks, '/process-marks')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)

# df = process_marks(student_file)
# df.to_csv('report.csv')
# for pg_num in range(num_of_pages):
#     pdf_text = pdf.getPage(pg_num).extractText()

#     match = re.search("(?<=GRADE POINTS1).*Letter Grades", pdf_text)
#     reduced_text = pdf_text[match.span()[0]:match.span()[1]]
#     lens = []
#     for key, val in reg_ex.items():
#             lens.append(len(re.split(val, reduced_text)[1:]))
#     print(re.split(reg_ex[lens.index(max(lens))], reduced_text)[1:])

# regular expressions 
# "Student:.*USN"
# "(?<=Student:).*USN"
# "Roll No:.*Branch"
# "GRADE POINTS.*Letter Grades"
# "[0-9]{3}[A-Z]{2}[0-9][A-Z]{5}"

# regex for splitting subject into marks
# "[0-9]{1}[A-Z]{1}[+]{0,1}"

# df['ENGINEERING MATHEMATICS II'] = None
# df['ENGINEERING PHYSICS'] = None
# df['BASIC ELECTRICAL ENGINEERING'] = None
# df['ELEMENTS OF CIVIL ENGINEERING AND MECHANICS'] = None
# df['ELEMENTS OF MECHANICAL ENGINEERING'] = None
# df['ENGINEERING PHYSICS LABORATORY'] = None
# df['WORKSHOP PRACTICE'] = None
# df['LANGUAGE LABORATORY Œ II (ENGLISH)'] = None

# df.loc['1DS18EC008', 'ENGINEERING MATHEMATICS II'] = 8
# df.loc['1DS18EC008', 'ENGINEERING PHYSICS'] = 7

# pdf = PyPDF2.PdfFileReader("/home/prajwal/Documents/Repositories/AutomatedResultProcessor/Marks_list/2sem_marks/1DS18EC008.pdf")
# text = pdf.getPage(0).extractText()
# match = re.search(r"GRADE POINTS.*Letter Grades", text)
# match.span()
# (1119, 1495)
# reduced_text = text[match.span()[0]:match.span()[1]]

# Course Code
# split_match = re.split(r"[0-9]{3}[A-Z]{2}[0-9][A-Z]{5}", reduced_text)
# split_match = re.split(r"[A-Z]{2,3}[0-9]{2,3}", reduced_text)
# split_match = re.split(r"[0-9]{2}[A-Z]{3,5}[0-9]{2,3}", reduced_text)
# re.finditer(reg, reduced_text)
# i.group() to get the match

# split_match[-1], gpa = split_match[-1].split('SGPA')
# split_match = split_match[1:]
# re.split(r"[0-9]{1,2}", ex)
# ['ENGINEERING MATHEMATICS Œ IV', 'S+', '']


# os.listdir(os.path.abspath('downloads'))
# ['file2', 'file1', 'file3']

# for i in range(pdf.getNumPages()):
#     text = pdf.getPage(i).extractText()
#     match = re.search("(?<=GRADE POINTS1).*Letter Grades", text)
#     reduced_text = text[match.span()[0]:match.span()[1]]
#     lens = []
#     for key, val in reg_ex.items():
#             lens.append(len(re.split(val, reduced_text)[1:]))
#             # print(key,val)
#             # print(re.findall(val, reduced_text), len(re.findall(val, reduced_text)))
#             # print(re.split(val, reduced_text)[1:], len(re.split(val, reduced_text)[1:]))
#     print(reg_ex[lens.index(max(lens))])
#     print(re.split(reg_ex[lens.index(max(lens))], reduced_text)[1:])
#     print("----------------")