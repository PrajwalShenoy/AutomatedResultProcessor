import sqlite3 as sq
import PyPDF2
import re

f = open('sem_marks.txt', 'w')

USN_LIST = open('list_students.txt', 'r')

conn = sq.connect('Marks.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Marks')
cur.execute('CREATE TABLE Marks (Name TEXT, USN TEXT, DC TEXT, ESD TEXT, FOVLSI TEXT, ITC, ELEC1 TEXT, ELEC2 TEXT, ADCL TEXT, VLSIL TEXT, SGPA TEXT)')

subjects = ['Name','USN','DC', 'ESD', 'FOVLSI', 'ITC', 'ELEC1', 'ELEC2', 'ADCL', 'VLSIL']

##for usn in range(0,1):
for usn in USN_LIST:
    #file = "marks\\1DS16EC"
    #name = file + str(usn) +".pdf"
    usn = usn.rstrip()
    print(usn)
    name = usn+".pdf"
    read = PyPDF2.PdfFileReader(name)
    page = read.getPage(0)
    content = page.extractText()
    data = []
    try:
        sub_num = 0
        vara = 0
        student_name = (re.findall("Student:(.*)USN", content)[0])
        student_usn = ((re.findall("Roll No:(.*)Branch", content)[0]))
        f.write(student_name)
        data.extend([student_name, student_usn])
        f.write("\t")
        f.write(student_usn)
        for i in content.split():
            string = i
            x = re.findall("[A-Z]+", string)
            y = re.findall("\d", string)
            if len(x) > 2:
                if len(y) > 1:
                    if y[0] in [ '2', '3', '4']:
                        if y[1] == "1":
                            jj = ("\nS+   10   " + y[0])
                            data.append('S+')
                            f.write(jj)
                            vara =vara + (int(y[0])*10)
                            sub_num = sub_num +1
                        else:
                            ii = ("\n"+x[1]+"    " + y[1]+"    " + y[0])
                            data.extend(x[1])
                            f.write(ii)
                            vara =vara +  (int(y[0])*int(y[1]))
                            sub_num = sub_num + 1
        f.write('\nSGPA ')
        data.append(str(vara/25))
        f.write(str(vara/25))
        f.write('\n\n')
        cur.execute('INSERT INTO Marks (Name, USN, DC, ESD, FOVLSI,ITC,ELEC1,ELEC2,ADCL,VLSIL,SGPA) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))
        print(data)
        conn.commit()
        
    except:
        conn.commit()
        continue

f.close()
cur.close()
print("done")

