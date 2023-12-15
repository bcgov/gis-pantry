'''
# Author:
# Ministry, Division, Branch:
# Created Date: 
# Updated Date: 
# Description:

--------------------------------------------------------------------------------
# * SUMMARY

# - INPUTS

# - OUTPUTS

--------------------------------------------------------------------------------
# * IMPROVEMENTS
* Suggestions...
--------------------------------------------------------------------------------
# * HISTORY

  Date      Initial/IDIR  Description
| ------------------------------------------------------------------------------
  yyyy-mm-dd    iii       Yada yada yayaya yada yayayay yada yada yada ya ya ya,
                          etc., etc.
  yyyy-mm-dd    iii       etc., etc.

'''

# *** IMPORTS ***
import arcpy
import sys, os
from pathlib import Path


# *** DEBUG ***
# debug and testing variables, decorators, and other script specific items...

TESTING = False
DECORATOR = '+-'*50
DEBUG = False


# *** ENVIRONMENTS ***
# environment set up...

arcpy.env.overwriteOutput = True


# *** PARAMETERS ***
# Script parameters, constants, environment variables...


# derived / programmatic  parameters
NOW = datetime.datetime.now()
NOW = now.strftime("%Y%m%d_%H%M%S")


# *** FUNCTIONS / CLASSES ***
# put functions and classes here...

# example with doc string template
def function_name(num1, num2):
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


# *** MAIN ***
if __name__ == __main__:
    # main code here...

    # 1. SECTION TITLE
    # +---------------------------------------------------------------------------------------------

    # SUBSECTION TITLE

    # Minor Subsection Title

    # If statement with a verbose doc string. For when you need more than a couple lines using '#' 
    if some_condition = True:
        '''
        Function, Class, If, Loop, etc. comment block. Info about what the thing is all about...
        more to say 
        more to say.... yada yada
        '''

    ## -- ANOTHER SUBSECTION
    # example showing how to wrap the substantial scripting in multiple try/except statements...
    try:
        '''
        Just showing the use of the above, but within an over-arching try statement
        that can wrap the entire script.
        '''
        # 1. SECTION TITLE
        # +-----------------------------------------------------------------------------------------

        # SUBSECTION TITLE

        # Minor Subsection Title

        try:
        except ValueError as e:
            '''
            do something here to handle it... 
                    OR
            re-raise to catch it in the higher level except
            '''
            raise ValueError('message here if you want')

    except ValueError:
        '''example of catching a specific type of error'''

    except Exception as e:
        '''catch-all exception'''

    finally:
        '''
        closeout code
        often good to have, but not always needed
        '''
