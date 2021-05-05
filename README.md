# Installing and using the tool

## Installing the tool
* Current working directory should be `./webapp/`
* Install all the required libraries using `pip install -r requirements.txt`

## Using the tool
* Current working directory should be `./webapp/`
* run `python get_marks.py` to download the result PDF results.
  - This should start a server on the local system.
  - Go to `localhost:5000` on your web browser, follow the prompt and upload the student list **student list should be in .txt format**
  - This will take a while, get yourself some tea while the download proceeds.
  - The downloaded files will be present in `./webapp/downloads`
* run `python process_marks.py` to generate the .csv file containing the spreadsheet
  - This should start a server on the local system.
  - Go to `localhost:5001` on your web browser, follow the prompt and upload the student list **student list should be in .txt format**
  - The following .csv file should be downloaded when `upload` button is clicked.
  - Check `./webapp/reports` for the processed .csv files.
* Remember to stop the running programs when you are done using it. :)


Format of the `.txt` file
```
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
```
