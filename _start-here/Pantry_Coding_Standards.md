***Last Update: 2023-12-06***   
***Tags: #code-standards***

# Basic Coding Standards & Best Practices
This document contains standards and guidelines for projects being shared to the GIS Pantry Github. These standards can also be used in all your projects. Many of these settings can be automatically applied to your VS Code projects using the project templates accompanying this read me. 

## Read-Me Files
Read-Me files are very helpful. GitHub will automatically display the contents of a readme file when a user views an folder.

You can add a README file to your directory to tell other people why your code is useful, what they can do with it, and how they can use it.

The link below is about readme files for repositories, but a lot of what it says easily translates to smaller entries.

[**GitHub Recommendations for read-me files**](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## What <ins>**NOT**</ins> to Include in your Github Repository
The GIS Panty is a public repository so it is important to review your files for any sensitive information before sharing your project.

- Filepaths to government network drive locations
- Employee names or contact information
- Usernames and passwords

## General Formatting
**First off >> [Here is a template file structure with template scripts](sample_project)**

### General Guidelines
- Be mindful and consistent with whitespace 
- Max line length should be 120 characters
    - ***Pep8 recommends 79 characters because it makes it easier to have multiple files open next to each other.***
- Use UNC paths unless the path is longer than 256 characters. On GitHub paths should be parameterized. 
    - ***This is for working project files, please remove all paths before sharing on Github!***  

**Here is an excellent primer on coding standards:**  
["How to Write Beautiful Python Code With Pep8"](https://realpython.com/python-pep8/)


## Naming Conventions
- snake_case for file names, variables, and functions
- TitleCase for classes
- CAPITAL_CASE for constants
- descriptive names for variables, functions, and classes
- f-strings instead of concatenation

~~~python
# Example naming conventions

from module_name import * # snake_case for file names/modules

variable_name = a+b # snake_case for variables

def function_name(): # snake_case for functions
    pass

CONSTANT_NAME = 1 # CAPITAL_CASE for constants

class ClassName: # TitleCase for classes
    pass

f"{variable_name} is a variable" # use f-strings instead of concatenation
~~~


## Commenting

- Use docstrings (triple quotes) for commenting functions (see Functions section below)
- Use a new line for comments over 120 characters
    - *pep8 recommends for 72-79 chars*
- Use block comments for comments that span more than one line 
- Use inline # comments for single lines of code sparingly 
- Comments should describe the reasoning for your process if it is unusual and/or complex 
    
~~~python
# Block Comments look like this:
# commenting out each line on a multi-line comment
# instead of using triple quotes

my_line_of_code = "string" # Inline comments look like this. They should be used sparingly.
~~~

### Script Header
Some basic information should be included in the header of all files to provide important information on understanding the document. The example below can also be found in the project template files. All file headers should include at least the following:

~~~python
# Author: Author(s) Name and Branch/Team
# Date Created: Date Created and/or Modified
# Description: 
#   Description of the scripted process. The reader should be able to 
#   understand the general inputs, outputs, process, and purpose of the 
#   script without reading the code.
~~~
Additionally headers could note limitations, any non-standard dependencies, special instructions for running the script, and any other information that would be useful to the user.

### Section Headers
Use section headers to split up substantially different sections of the script for long/complex code to make it easier to read and search. 

~~~python
# Section Title Information
# --------------------------------------------------------------------------------------------------
~~~

## Functions
- In general, it is better if functions are short and reusable but longer single use functions can be used if necessary
- Try to organize repetitive tasks into functions. If multiple processes are similar enough, they should be implemented in a function with differences being handled by input variables.
- Always have a docstring except for the most obvious of functions as described above. 
### Function Docstrings
- Always have a docstring except for the most obvious of functions 
- An example can be found below or in the project template python files
- For more examples and information on function docstrings: 
https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e

~~~python
def multiply_numbers(num1, num2):
    """
    Multiplies two input numbers and returns the result

    Args: 
        num1 (int, float): 1st number 
        num2 (int, float): 2nd number
    
    Returns: 
        result (int, float): multiplication result

    Example:
        result = multiply_numbers(2, 3)
    """

    result = num1 * num2
    return result
~~~

## File Structure
- Imports, parameters, functions at the top for shorter scripts
- As much as possible, it should be easy to find parameters and functions, make changes in only one obvious location, and have the script still work
- Separate large scripts into multiple files. An example would be:
    - config.py
    - functions.py
    - main.py
- If you're constantly scrolling through your script to find something, it's probably time to split it up.
- Data stored separately from project and especially not in GitHub. 
- Some examples of data files includes: geospatial data, spreadsheets, etc.

**Again [here is a template file structure with template scripts](sample_project)**