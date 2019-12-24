import sqlite3 as sq
import PyPDF2
import re
import os
import shutil
from tabula import read_pdf
from tabulate import tabulate

USN_LIST = open('6sem_students.txt' , 'r')
faults = 0
fault_list = []
success = 0

path = 'test.sqlite'
conn = sq.connect(path)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS PrajwalsMarks')
cur.execute("""CREATE TABLE PrajwalsMarks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
             Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, GPA TEXT)""")

for USN in USN_LIST:
    # USN = '1DS16EC096'
    USN = USN.rstrip()
    try:
        complete_table = read_pdf('6sem_marks/' + USN + '.pdf')
        selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
        table_to_list = selective_table.values.tolist()
        read = PyPDF2.PdfFileReader('6sem_marks/' + USN + '.pdf')
        page = read.getPage(0)
        content = page.extractText()
        student_name = re.findall("Student:(.*)USN", content)[0]
        # print(student_name)
        marks = []
        for i in range(0, len(table_to_list)-1):
            marks.append(table_to_list[i][1])
        cur.execute('INSERT INTO PrajwalsMarks (Name, USN) VALUES (?, ?)', (student_name, USN))
        cur.execute('''UPDATE PrajwalsMarks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, GPA = ?  WHERE name = ?'''
                    ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], table_to_list[len(table_to_list)-1][2], student_name))
        success = success + 1
        print(USN)
    except:
        print(USN + " did not get added")
        faults = faults + 1
        fault_list.append(USN)
conn.commit()

print("total number of success = " + str(success))
print("total number of faults = " + str(faults))
for i in fault_list:
    print(i)
# UPDATE Users SET name="Charles" WHERE email='csev@umich.edu'
