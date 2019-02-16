# QOL Module 

Python module with a number of misc functions and classes, mostly quality of life functions to addi small bits of functionality to other programs.

## To Do
## TimeTaken 
Class that can be used to calculate the time taken for a program to run contains various methods. Will contain these functions
- __init__ - initialise the timer by getting the current time and saving it.
- resetTime - overwrites the saved start time with the current time to reset the timer
- getTimeTaken - returns a string with the amount of time passed since the saved start time, outputs the string in a readable format including hours, minutes and seconds
## LoopCounter 
Class that can be used in a similar way to tqdm, in that it will count loops and return a string with the loop numver, total loops and percentage. Contains these functions:
- __init__ - this will initialise the counter and takes the total number of loops, a counter description and sets the current loop to 1
- getCount - outputs a string containing the current loop out of the total (inc percentage), then adds 1 to the current loop
- resetCount - this will reset the current loop to 1 and accept a new total counts and description
