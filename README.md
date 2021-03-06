# AutomatedResultProcessor
Automates the processing of result .pdf files into a SQL database.

Steps to use the program.
1) Installation of the latest distribution of Python3
		Steps to install Python3
		Windows users  
		- Visit https://www.python.org/downloads/windows/  
		- Select the lates verion of Python for download.  
		- Run the downloaded installer.  
		- In the first page DO NOT FORGET to select the "Add Python 3.7 to path"  
		- Proceed through the steps as directed by the installer.  
		- Verify installation by searching for "IDLE" in the windows search option.  
2) Installing a SQL database browser.  
		- Visit https://sqlitebrowser.org/dl/  
		- Download the version appropriately and install accordingly.  
3) Installing pre requisite libraries  
		- Open the "Run" window by pressing  "WIN + R" on the keyboard.  
		- Type "cmd" and press "Enter"  
		- Execute the following commands as entered below.  
				- pip3 install requests  
				- pip3 install PyPDF2  
				- pip3 install tabula-py  
				- pip3 install tabulate  
				- pip3 install PyQt5  
4) Initialise Student information for smooth functioning.  
		Student_list  
			- "Student_list" consists of 8 ".txt" files.  
			- Each of these files contains the list of "Student USN".  
			- For exact format of these ".txt" files refer appendix-1 below.  
		Marks_list  
			- "Marks_list" consists of 8 files from "1sem_marks" through "8sem_marks".  
			- These files hould be emptied before running the "getMarks.py" program.  
			- "getMarks.py" downloads and saves the result pdf's in these folders.  
			- After running "getMarks.py" these folders are not to be manipulated.  
5) Steps to obtain the results after processing.  
		- Setup the Student_list file  
				- Select the semester you want to process the results of, eg-6th semester.  
				- Double click the "6sem_students.txt" file.  
				- Enter the USN list according to Appendix-1  
				- Save the files  
		- Run the "getMarks.py" program by double clicking the file.  
				- On the prompt enter the semester, eg - 6  
				- Press "Enter", all the .pdf files are downloaded.  
				- These pdf's can be found in "Marks_list" under the respective folder.  
		- Run the "computeMarks.py" program by double clicking the file.  
				- Select the semester using the Semester selector in the application window.  
				- Click the "Process" button to start computing the marks.  
				- On the progress bar reaching 100% log information is printed.  
				- Exit the program  
		- Access the database from the "Marks_excel" folder.  
				- The folder should contain the "6sem_marks.sqlite" file.  
				- Double clicking on the file should open the database.  
				- Select "Browse Data" to view your data.  
				- This data can be copied to an excel sheet using copy-paste functions.  

Appendix  
Appendix 1  
Format of the .txt files.  
1DS15EC023  
1DS15EC139  
1DS16EC011  
1DS16EC014  
1DS16EC015  
1DS16EC023  
1DS16EC034  
1DS16EC037  
1DS16EC041  
1DS16EC047  
1DS16EC048  
1DS16EC050  
1DS16EC056  
1DS16EC059  
1DS16EC062  
1DS16EC065  
1DS16EC066  
1DS16EC067  
1DS16EC072  

Appendix 2  
		- "log_files.txt" contains important information like  
				- Time take to process  
				- USN list that could not be processed.  
				- Number of success and number of failures.  

Notes.  
This application returns the list of USN whose results couldnt be processed due to various reasons.  
These results need to be manually entered in to the database.  
This application has been succesfullt tested on semesters 2,4,6,8.
For clarification on the applications reach out to prajwalkpshenoy@gmail.com  
