import requests
import os

semester = input("Enter the semester number: ")

f = open('Student_list\\' + semester + 'sem_students.txt', 'r')

URL_FORMAT = 'http://45.32.111.231:8080/birt/frameset?__report=mydsi/exam/Exam_Result_Sheet_dsce.rptdesign&__format=pdf&USN='
# URL_FORMAT = 'http://45.32.111.231:8080/birt/frameset?__report=mydsi/exam/Exam_Result_Sheet_dsce.rptdesign&__format=pdf&USN='
FILE_FORMAT = str(os.path.abspath('')) + '\\Marks_list\\' + semester + 'sem_marks\\'

# FILE_FORMAT= '/home/prajwal/Desktop/marks_linux/Project_auto_marks/Marks_list/' + semester + 'sem_marks/'
print("Downloading...")

for usn in f:
    usn = usn.rstrip()[:10]
    print(usn)
    r = requests.get(URL_FORMAT + usn)
    if r.status_code != 200:
        continue

    with open(FILE_FORMAT + usn + '.pdf', 'wb') as f:
        f.write(r.content)
print("Task completed...")
