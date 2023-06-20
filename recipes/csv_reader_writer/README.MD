#Dictionary List Format
Dictionary lists are created from CSV files with the following format. 
Each list item represents a row of data in the csv where the KEYS are the 
COLUMN HEADERS and the VALUES are the column values for the current row

[{COL1 HEADER: COL1 VALUE, COL2 HEADER: COL2 VALUE, etc},
 {COL1 HEADER: COL1 VALUE, COL2 HEADER: COL2 VALUE, etc},
 {COL1 HEADER: COL1 VALUE, COL2 HEADER: COL2 VALUE, etc}]

#PYTHON VERSION COMPATIBILITY
This code contains a version check for Python 2.x or 3.x and selects the appropriate formatting