from flask_restx import Resource, reqparse, Namespace
from get_marks import UPLOAD_FOLDER, DOWNLOADS_FOLDER
from werkzeug.datastructures import FileStorage
from flask import request, send_file
from get_marks import receive_upload
import pandas as pd
import PyPDF2
import os
import re


api = Namespace('processMarks', description="Generates .csv report")

def get_upload_parser():
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument("student_list", location='files', type=FileStorage, required=False)
    upload_parser.add_argument('point_system', location='form', type=str, required=False, help="Options = true")
    return upload_parser

upload_parser = get_upload_parser()

REPORTS_FOLDER = os.path.abspath('reports')

reg_ex = {0: "[1-9]{2}[A-Z]{2}[0-9][A-Z]{5}",
          1: "[A-Z]{2,3}[1-9]{2}",
          2: "[1-9]{2}[A-Z]{3,5}[1-9]{2,3}",
          3: "[A-Z]{6}[0-9]{2,3}",
          4: "[1-9]{2}[A-Z]{2}[0-9][A-Z]{4,5}[0-9]{0,1}"}

@api.route("/process-marks")
class ProcessMarks(Resource):
    """Generates .csv file"""

    @api.expect(upload_parser)
    def post(self):
        try:
            points = request.form.get('point_system', '')
            files_uploaded = receive_upload(request)
            if files_uploaded[0]:
                if verify_downloads(files_uploaded[1]):
                    df = process_marks(files_uploaded[1], points)
                    process_df(df, files_uploaded[1])
                    return send_file(os.path.join(REPORTS_FOLDER, files_uploaded[1][:-3]+'.csv'))
                else:
                    return {'error': 'Some files are not present, please re-download them'}
            else:
                return {'error': 'File could not be uploaded'}
        except:
            return {'error': 'Something is wrong'}

def process_df(df, file_name):
    df.to_csv(os.path.join(REPORTS_FOLDER, file_name[:-3]+'.csv'))

def verify_downloads(student_file):
    file_list = os.listdir('downloads')
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
        for student in student_list:
            if student.rstrip() + '.pdf' not in  file_list:
                return False
    return True

def process_marks(student_file, points=False):
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
                    df = process_page(pdf, pg_num, df, student.rstrip(), points)
            except:
                print("Could not process", student)
    return df

def process_page(pdf, pg_num, df, student, points=False):
    pdf_text = pdf.getPage(pg_num).extractText()
    df.loc[student, 'Name'] = re.search("(?<=Student:).*USN", pdf_text).group()[:-3]
    match = re.search("(?<=GRADE POINTS1).*Letter Grades", pdf_text)
    reduced_text = pdf_text[match.span()[0]:match.span()[1]]
    split_match = re.split(select_regex(reduced_text), reduced_text)[1:]
    split_match[-1], sgpa = split_match[-1].split('SGPA')
    df.loc[student, 'SGPA'] = sgpa.split('L')[0]
    split_match = [subject[:-1] for subject in split_match[:-1]] + [split_match[-1]]
    print(split_match)
    if points:
        split_match = [re.split("[0-9]{1}[A-Z]{1,2}[+]{0,1}", subject) for subject in split_match]
    else:
        re_exp = [re.search("[0-9]{1}[A-Z]{1,2}[+]{0,1}", subject) for subject in split_match]
        tmp = []
        for i in range(len(re_exp)):
            tmp.append([split_match[i][:re_exp[i].start()], split_match[i][re_exp[i].span()[0]+1:re_exp[i].span()[1]]])
        split_match = tmp
    print(split_match)
    df = check_for_sub_heading(split_match, df)
    df = update_marks(split_match, df, student)
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

