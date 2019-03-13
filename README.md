# QOL Module 

Python module with a number of misc functions and classes, mostly quality of life functions to addi small bits of functionality to other programs.

## Functions
### TimeTaken 
Class that can be used to calculate the time taken for a program to run contains various methods. Will contain these functions
- __init__ - initialise the timer by getting the current time and saving it.
- resetTime - overwrites the saved start time with the current time to reset the timer
- getTimeTaken - returns a string with the amount of time passed since the saved start time, outputs the string in a readable format including hours, minutes and seconds
## To Do
### LoopCounter 
Class that can be used in a similar way to tqdm, in that it will count loops and return a string with the loop numver, total loops and percentage. Contains these functions:
- __init__ - this will initialise the counter and takes the total number of loops, a counter description and sets the current loop to 1
- getCount - outputs a string containing the current loop out of the total (inc percentage), then adds 1 to the current loop
- resetCount - this will reset the current loop to 1 and accept a new total counts and description
### Doc converter
Function that can convert the docstrings from a python file into a readme type document for explaining what the functions and classes do.
### Readme
Update this readme with more details explaining the functions and classes present, possibly done using the doc converter function mentioned above.
### Old module QOL
Add some more of the functions from my old module QOL file.
### Add gitignore file
Add gitigore file to ignore any irrelevant such as test files and the __pycache__ folder.
