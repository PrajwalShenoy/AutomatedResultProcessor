# Installing and using the tool

## Installing the tool
* Current working directory should be `./webapp/`
* Install all the required libraries using `pip install -r requirements.txt`

## Using the tool
* Current working directory should be `./webapp/`
* run `get_marks.py` to download the result PDF results.
  - This should start a server on the local system.
  - Go to `localhost:5000` on your web browser, follow the prompt and upload the student list **student list should be in .txt format**
  - This will take a while, get yourself some tea while the download proceeds.
  - The downloaded files will be present in `./webapp/downloads`
* run `process_marks.py` to generate the .csv file containing the spreadsheet
  - This should start a server on the local system.
  - Go to `localhost:5001` on your web browser, follow the prompt and upload the student list **student list should be in .txt format**
  - The following .csv file should be downloaded when `upload` button is clicked.
  - Check `./webapp/reports` for the processed .csv files.
* Remember to stop the running programs when you are done using it. :)
