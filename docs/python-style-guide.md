# Basic Coding Standards 

## Best Practices 

### Formatting: 

* snake_case for variables, functions, and file names 
* TitleCase for classes 
* CAPITAL_CASE for constants 
* Use f"{strings}" instead of concatenation 
* Be mindful and consistent with whitespace 
* max line length should be roughly 79 characters 
* more here: https://realpython.com/python-pep8/ 
* Use UNC paths unless path is longer than 256 characters 
* Possible: Should we standardize path formatting? EG os.path.join(), format strings? Something else? 

### Commenting: 

* ensure at least your main file has a header with author, your branch/team, date modified, and description 
* Use docstrings (triple quotes) for commenting functions 
* Use a new line if comments get over 79 characters 
* Use 	# block comments for comments 
    ```
    # that span is more than
    # one line
    ```

* Use inline `#` comments for single lines of code sparingly 
* Comments should describe the reasoning for your process if it’s unusual and/or complex 
* Use section headers to split up substantially different sections of the script for long/complex code to make it easier to read and search: 
```
# Section Title Information 

# ---------------------------------------------------
```
 
### Functions: 

* In general, it’s better if functions are short and reusable but longer single use functions can be used if necessary 
* Try to organize repetitive tasks into functions. If multiple processes are similar enough, they should be implemented in a function with differences being handled by input variables. 
* Always have a docstring except for the most obvious of functions 
* Function docstrings formatting: [https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e]()
 

### File structure: 

* Imports, parameters, functions at the top for shorter scripts 
* Separate large scripts into multiple files. An example would be: 

    * config.py 
    * functions.py 
    * main.py 

* As much as possible, it should be easy to find parameters and functions, make changes in only one obvious location, and have the script still work.  

## Resources to Build 

### VS Tips/Suggestions document 

* Suggested extensions 
* What formatter to use 
* Ruler settings 

### VS Code Project Template 

* Standardized header 
* Customized formatter set up 
* Ruler widths etc. set up  
* Etc. 

 