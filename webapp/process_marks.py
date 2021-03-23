from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
import pandas as pd
import os
import requests
import PyPDF2
import re


# regular expressions 
# "Student:.*USN"gm
# "Roll No:.*Branch"gm
# "GRADE POINTS.*Letter Grades"gm
# "[0-9]{3}[A-Z]{2}[0-9][A-Z]{5}"gm

# >>> df['ENGINEERING MATHEMATICS II'] = None
# >>> df['ENGINEERING PHYSICS'] = None
# >>> df['BASIC ELECTRICAL ENGINEERING'] = None
# >>> df['ELEMENTS OF CIVIL ENGINEERING AND MECHANICS'] = None
# >>> df['ELEMENTS OF MECHANICAL ENGINEERING'] = None
# >>> df['ENGINEERING PHYSICS LABORATORY'] = None
# >>> df['WORKSHOP PRACTICE'] = None
# >>> df['LANGUAGE LABORATORY Œ II (ENGLISH)'] = None

# >>> df.loc['1DS18EC008', 'ENGINEERING MATHEMATICS II'] = 8
# >>> df.loc['1DS18EC008', 'ENGINEERING PHYSICS'] = 7