# Dictionary List Format

Dictionary lists are created from CSV files with the following format. 
Each list item represents a row of data in the csv where the KEYS are the 
COLUMN HEADERS and the VALUES are the column values for the current row.

## CSV Example

| COL1 HEADER | COL2 HEADER |
| ----------- | ----------- |
| ROW1 VALUE1 | ROW1 VALUE2 |
| ROW2 VALUE1 | ROW2 VALUE2 |

## Dictionary List Example

```
[{COL1 HEADER: ROW1 VALUE1, COL2 HEADER: ROW1 VALUE2, etc},
 {COL1 HEADER: ROW2 VALUE2, COL2 HEADER: ROW2 VALUE2, etc},
 continues for all rows...]
```

## PYTHON VERSION COMPATIBILITY

This code contains a version check for Python 2.x or 3.x and selects the appropriate formatting
