import sqlite3 as sq
import PyPDF2
import re
import os
import shutil
import time
from tabula import read_pdf
from tabulate import tabulate
from datetime import datetime

def computeMarksList(semester):
    startTime = time.time()
    USN_LIST = open(os.path.abspath("Student_list") + '/' + semester + "sem_students.txt", 'r')
    faults = 0
    fault_list = []
    success = 0

    path = os.path.abspath("Marks_excel") + '/' + semester +"sem_marks.sqlite"
    conn = sq.connect(path)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Marks')
    if semester == '6':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, GPA TEXT)""")
        for USN in USN_LIST:
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '/' + semester + "sem_marks" + '/' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '/' + semester + "sem_marks" + '/' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                for i in range(0, len(table_to_list)-1):
                    marks.append(table_to_list[i][1])
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], table_to_list[len(table_to_list)-1][2], student_name))
                success = success + 1
                print(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '8':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Project TEXT,
                     TechinacalSeminar TEXT, Cred2 TEXT, GPA TEXT)""")
        for USN in USN_LIST:
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '/' + semester + "sem_marks" + '/' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '/' + semester + "sem_marks" + '/' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                for i in range(0, len(table_to_list)-1):
                    marks.append(table_to_list[i][1])
                # gpa = ((int(table_to_list[0][2])*3) + (int(table_to_list[1][2])*3) + (int(table_to_list[2][2])*15) + (int(table_to_list[3][2])*2) + (int(table_to_list[4][2])*2))/25
                try:
                    gpa = table_to_list[len(table_to_list)-1][2]
                except:
                    gpa = ""
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Project = ?, TechinacalSeminar = ?, Cred2 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], gpa, student_name))
                success = success + 1
                print(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
# --------------------------------------------------------------------------------------------------------------------------------------
    conn.commit()
    logFile = open("log_files.txt", 'a')
    logFile.write("--------------------------------------------------------" + '\n')
    logFile.write("processing of semester: " + semester + "\n")
    logFile.write(str(datetime.now())[:-7] + "\n")
    logFile.write("total number of success = " + str(success) + '\n')
    logFile.write("total number of faults = " + str(faults) + '\n')
    for i in fault_list:
        logFile.write(i + '\n')
    logFile.write("Time taken: " + str(time.time() - startTime) + "seconds" + "\n")
    logFile.close()
    print("--------------------------------------------------------")
    print("total number of success = " + str(success))
    print("total number of faults = " + str(faults))
    for i in fault_list:
        print(i)
    print("--------------------------------------------------------")

# --------------------------------------------------------------------------------------------------------------------------------------

inputSemester = input("Enter the semester to be processed: ")
computeMarksList(inputSemester)
