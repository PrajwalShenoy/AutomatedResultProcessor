from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
import pandas as pd
import os
import requests
import PyPDF2
import re


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

# test = PyPDF2.PdfFileReader("/home/prajwal/Documents/Repositories/AutomatedResultProcessor/Marks_list/2sem_marks/1DS18EC008.pdf")
# text = test.getPage(0).extractText()
# match = re.search(r"GRADE POINTS.*Letter Grades", text)
# match.span()
# (1119, 1495)
# reduced_text = text[match.span()[0]:match.span()[1]]
# split_match = re.split(r"[0-9]{3}[A-Z]{2}[0-9][A-Z]{5}", reduced_text)
# split_match[-1], gpa = split_match[-1].split('SGPA')
# split_match = split_match[1:]
# re.split(r"[0-9]{1,2}", ex)
# ['ENGINEERING MATHEMATICS Œ IV', 'S+', '']