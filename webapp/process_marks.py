from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from get_marks import receive_upload, allowed_filename
from get_marks import UPLOAD_FOLDER, DOWNLOADS_FOLDER, ALLOWED_EXTENSIONS
import pandas as pd
import os
import requests
import PyPDF2
import re

class veri(Resource):


def verify_downloads(student_file):
    file_list = os.listdir('downloads')
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
        for student in student_list:
            if student.rstrip() + '.pdf' file_list:
                continue
            else:
                return {'error': 'Some files are not present, please re-download them'}
    return True

def process_marks(student_file):
    df = pd.DataFrame()
    with open(os.path.join(UPLOAD_FOLDER, student_file)) as student_list:
        for student in student_list:
            pdf = PyPDF2.PdfFileReader(os.path.join(DOWNLOADS_FOLDER, student.rstrip()+'.pdf'))
            num_of_pages = pdf.getNumPages()
            for pg_num in range(num_of_pages):
                process_page(pdf, pg_num, df)

def process_page(pdf, pg_num, df):


def check_and_columns():


# regular expressions 
# "Student:.*USN"
# "Roll No:.*Branch"
# "GRADE POINTS.*Letter Grades"
# "[0-9]{3}[A-Z]{2}[0-9][A-Z]{5}"

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