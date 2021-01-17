import sqlite3 as sq
import PyPDF2
import re
import os
import shutil
import time
import warnings
from tabula import read_pdf
from tabulate import tabulate
from datetime import datetime

from PyQt5 import QtWidgets, uic, QtCore, QtGui

# import front_page

warnings.filterwarnings("error")

def computeMarksList(semester):
    startTime = time.time()
    USN_LIST = open(os.path.abspath("Student_list") + '\\' + semester + "sem_students.txt", 'r')
    numberOfLines = 0
    for i in USN_LIST:
        numberOfLines = numberOfLines + 1
    forPer = 100/numberOfLines
    USN_LIST.close()
    USN_LIST = open(os.path.abspath("Student_list") + '\\' + semester + "sem_students.txt", 'r')
    faults = 0
    fault_list = []
    success = 0
    path = os.path.abspath("Marks_excel") + '\\' + semester +"sem_marks.sqlite"
    conn = sq.connect(path)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Marks')
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '2':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, GPA TEXT)""")
        pres = 0

        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            # USN = USN.rstrip()
            USN, student_name = USN.rstrip()[:10], USN.rstrip()[11:]
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"), pages=1)
                # selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
                table_to_list = complete_table[0]['GRADE.1'].tolist()[1:]
                # table_to_list = selective_table.values.tolist()
                # read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                # page = read.getPage(0)
                # content = page.extractText()
                # student_name = re.findall("Student:(.*)USN", content)[0]
                # marks = []
                # for i in range(0, len(table_to_list)-1):
                #     marks.append(table_to_list[i][1])
                marks = table_to_list
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], marks[-1], student_name))
                success = success + 1
                print(USN, student_name)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '3':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, Sub9 TEXT, Sub10 TEXT, GPA TEXT)""")
        pres = 0
        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['COURSE COURSE', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                for i in range(0, len(table_to_list)-1):
                    marks.append(table_to_list[i][1])
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                if len(marks) == 9:
                    cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, Sub9 = ?, Sub10 = ?, GPA = ?  WHERE name = ?'''
                                ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], marks[8], "NA", table_to_list[len(table_to_list)-1][2], student_name))
                if len(marks) == 10:
                    cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, Sub9 = ?, Sub10 = ?, GPA = ?  WHERE name = ?'''
                                ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], marks[8], marks[9], table_to_list[len(table_to_list)-1][2], student_name))
                success = success + 1
                print(USN)
            except FutureWarning:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '4':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, Sub9 TEXT, GPA TEXT)""")
        pres = 0
        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['COURSE COURSE', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                for i in range(0, len(table_to_list)-1):
                    if i != 7:
                        marks.append(table_to_list[i][1])
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                if len(marks) == 8:
                    cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, Sub9 = ?, GPA = ?  WHERE name = ?'''
                                ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], "NA", table_to_list[len(table_to_list)-1][2], student_name))
                if len(marks) == 9:
                    cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, Sub9 = ?, GPA = ?  WHERE name = ?'''
                                ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], marks[8], table_to_list[len(table_to_list)-1][2], student_name))
                success = success + 1
                print(USN)
            except FutureWarning:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '5':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, Sub9 TEXT, GPA TEXT)""")
        pres = 0
        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                # selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
                selective_table = complete_table.loc[1:, ['CREDITS', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                for i in range(0, len(table_to_list)-1):
                    marks.append(table_to_list[i][1])
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, Sub9 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], marks[8], table_to_list[len(table_to_list)-1][2], student_name))
                success = success + 1
                print(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '6':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, GPA TEXT)""")
        pres = 0
        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['COURSE.1', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
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
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '7':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Sub3 TEXT,
                     Sub4 TEXT, Sub5 TEXT, Sub6 TEXT, Sub7 TEXT, Sub8 TEXT, GPA TEXT)""")
        pres = 0
        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            USN = USN.rstrip()
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                selective_table = complete_table.loc[1:, ['CREDITS', 'GRADE', 'GRADE.1']]
                table_to_list = selective_table.values.tolist()
                read = PyPDF2.PdfFileReader(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"))
                page = read.getPage(0)
                content = page.extractText()
                student_name = re.findall("Student:(.*)USN", content)[0]
                marks = []
                if len(table_to_list) == 11:
                    for i in range(0, len(table_to_list)-1):
                        if i != 6:
                            if i != 8:
                                marks.append(table_to_list[i][1])
                else:
                    for i in range(0, len(table_to_list)-1):
                        if i != 7:
                            marks.append(table_to_list[i][1])
                # for i in range(0, len(table_to_list)-1):
                #     marks.append(table_to_list[i][1])
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Sub3 = ?, Sub4 = ?, Sub5 = ?, Sub6 = ?, Sub7 = ?, Sub8 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], marks[6], marks[7], table_to_list[len(table_to_list)-1][2], student_name))
                success = success + 1
                print(USN)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if semester == '8':
        cur.execute("""CREATE TABLE Marks (Name TEXT, USN TEXT, Sub1 TEXT, Sub2 TEXT, Project TEXT,
                     TechinacalSeminar TEXT, Cred2 TEXT, GPA TEXT)""")
        pres = 0

        for USN in USN_LIST:
            pres = int(pres + forPer)
            call.progressBar.setValue(pres)
            # USN = USN.rstrip()
            USN, student_name = USN.rstrip()[:10], USN.rstrip()[11:]
            try:
                complete_table = read_pdf(os.path.abspath("Marks_list" + '\\' + semester + "sem_marks" + '\\' + USN + ".pdf"), pages=1)
                table_to_list = complete_table[0]['GRADE.1'].tolist()[1:]
                marks = table_to_list
                cur.execute('INSERT INTO Marks (Name, USN) VALUES (?, ?)', (student_name, USN))
                cur.execute('''UPDATE Marks SET Sub1 = ?, Sub2 = ?, Project = ?, TechinacalSeminar = ?, Cred2 = ?, GPA = ?  WHERE name = ?'''
                            ,(marks[0], marks[1], marks[2], marks[3], marks[4], marks[-1], student_name))
                success = success + 1
                print(USN, student_name)
            except:
                print(USN + " did not get added")
                faults = faults + 1
                fault_list.append(USN)
        call.progressBar.setValue(100)
# --------------------------------------------------------------------------------------------------------------------------------------
    conn.commit()
    logFile = open("log_files.txt", 'a')
    logFile.write("--------------------------------------------------------" + '\n')
    logFile.write("processing of semester: " + semester + "\n")
    call.terminal_display.append("processing of semester: " + semester)
    logFile.write(str(datetime.now())[:-7] + "\n")
    call.terminal_display.append(str(datetime.now())[:-7])
    logFile.write("total number of success = " + str(success) + '\n')
    call.terminal_display.append("total number of success = " + str(success))
    logFile.write("total number of faults = " + str(faults) + '\n')
    call.terminal_display.append("total number of faults = " + str(faults))
    for i in fault_list:
        logFile.write(i + '\n')
        call.terminal_display.append(i)
    logFile.write("Time taken: " + str(time.time() - startTime) + "seconds" + "\n")
    call.terminal_display.append("Time taken: " + str(time.time() - startTime) + "seconds")
    logFile.close()
    print("--------------------------------------------------------")
    print("total number of success = " + str(success))
    print("total number of faults = " + str(faults))
    for i in fault_list:
        print(i)
    print("--------------------------------------------------------")

# --------------------------------------------------------------------------------------------------------------------------------------
def getSemSpinBox():
    semester_input = 0
    semester_input = call.sem_select.value()
    # call.terminal_display.append("Process initiated")
    computeMarksList(str(semester_input))
# inputSemester = input("Enter the semester to be processed: ")
# computeMarksList(inputSemester)
# front_page.executable()
app = QtWidgets.QApplication([])
call = uic.loadUi("front_page.ui")

call.progressBar.setValue(0)

# call.terminal_display.append("Program ready to start...")
# call.process_pushButton.clicked.connect(lambda: computeMarksList(str(call.sem_spinBox.value())))
call.process_pushButton.clicked.connect(lambda: getSemSpinBox())

call.show()
app.exec()
