# RTD Tea Collection Automation
Python script that searches [this database](https://ndb.nal.usda.gov/ndb/foods/) for products and gets their nutrition data.

Reference `rtd.xlsx` for data this script is pulling from. Searches using first four words of the title in the database.s

## Usage

Make sure you have python3 installed on your machine.

Install Dependencies:
`pip3 install -r requirements.txt`

Run Program:
`python3 script.py`

## Notes

This program is written terribly and needs some serious refactoring. This is more of a proof of concept then an actual finished program.

Theres a variety of TODOs in `script.py` if you're interested in refactoring.

Some General Improvements:
- Eliminate having to write and read xml files
- Write to same file by preserving dataframe that's inputed
- Add way to cross check data
- Flexible inputs for data row and how many inputs you want
- Translate some of the inputs from the xl table
  - Should be a simple if else statement

Some abbreviations I noted need to be fixed

| Abbreviation   | Translation     |
| :------------- | :-------------  |
| Gren           | Green           |
| GNSNG          | Ginseng         |
| SWT            | Sweet           |
| HNY            | Honey           |
| PMGRNT         | Pomegranate     |
| T - TE         | Tea             |
| PCH            | Peach           |
| WHT            | White           |
