# -*- coding: utf-8 -*-
"""
Module containing some Quality of life functions and classes.

Classes
----------
    TimeTaken
        Simple class for measuring the time taken for a program to run and outputting it in a readable way.
    Logger
        Class that will allow the user to log to a file while also printing to console
        
Functions
----------
    newDir
        Checks if all directories in a path exist and if not makes the missing ones.
"""
##### IMPORTS #####
import os
import time

##### CLASSES #####
class TimeTaken:
    """
        Simple class for measuring the time taken for a program to run and outputting it in a readable way.
    """
    def __init__(self):
        """Sets start to currect time when class is instanciated."""
        self.start = time.clock()
        return
        
    def getTimeTaken(self):
        """Returns a readable formatted string of the time taken."""
        #Calc time taken
        timeTaken = round(time.clock() - self.start)
        if timeTaken >= 60:
            timeTakenSecs = int(timeTaken % 60)
            timeTakenMins = int((timeTaken - timeTakenSecs) / 60)
            if timeTakenMins >= 60:
                timeTakenMins = int(timeTakenMins % 60)
                timeTakenHrs = int((timeTaken - (timeTakenMins * 60) - timeTakenSecs) / 3600)
                return "{} hrs, {} mins, {} secs.".format(timeTakenHrs, timeTakenMins, timeTakenSecs)
            else:
                return "{} mins, {} secs.".format(timeTakenMins, timeTakenSecs)
        elif timeTaken < 1:
            return "< 1 sec."
        else:
            return "{} secs.".format(timeTaken)
        
    def resetStart(self):
        """Resets the start time, returns new start time."""
        self.start = time.clock()
        return self.start

class Logger:
    """
        Class that will allow the user to log to a file while also printing to console, 
        inspired by the logging module albeit much simpler.
        
        Parameters
        ----------
        logFile: string
            Path to the log file.
        append: boolean, optional
            Whether or not to append to the logFile (True), if it already exists, or overwrite it (False).
            Default False.
        level: string, optional
            The level of message which to output to console, can be one of 4 values ('DEBUG', 'INFO', 'ERROR', 'FATAL').
            Default 'INFO'.
        tags: boolean, optional
            Whether to include [time][level] on each line of the log file.
            Default True.
    """
    # Class variables
    lvlVals = {'DEBUG':0, 'INFO':1, 'ERROR':2, 'FATAL':3}
    
    def __init__(self, logFile, append=False, level='INFO', tags=True):
        """Initialises the class and sets the console output level and the path to the log file."""
        self.logFile = logFile
        self.setLevel(level)
        self.incTags = tags
        # Select mode
        if not append:
            mode = 'wt'
        else:
            mode = 'at'
        # Create log file (if it doesn't exist already)
        with open(logFile, mode):
            pass
        
        return
        
    def setLevel(self, level):
        """
            Set the console output level to a new value.
            
            Parameters
            ----------
                level: string, optional
                    The level of message which to output to console, can be one of 4 values ('DEBUG', 'INFO', 'ERROR', 'FATAL').
                    Default 'INFO'.
        """
        # Check level is an acceptable value
        if level.upper() not in Logger.lvlVals.keys():
            raise ValueError('level not acceptable value, given {} should be {}'.format(level, Logger.lvlVals.keys()))
        self.consoleLvl = level.upper()
        return
    
    def getLevel(self):
        """Returns the current console output level."""
        return self.consoleLvl
    
    def getTime(self):
        """Returns the current time and date as a string"""
        t = time.localtime()
        return '{:0>2}/{:0>2}/{:0>2} {:0>2}:{:0>2}:{:0>2}'.format(t[2], t[1], str(t[0])[2:4], t[3], t[4], t[5])
    
    def printOut(self, *args, level='INFO', newLine=False):
        """
            Prints out a message to the console, if level is above console output level, and to the log file.
           
            Parameters
            ----------
                *args: string or multiple strings
                    String to be printed and written to log file.
                level: string, optional
                    The level of importance of the message. Default 'INFO'.
                newLine: boolean, optional
                    Whether or not to put each argument on a new line. Default True.
        """
        level = level.upper()
        # Print if level is greater than console level
        try:
            if self.lvlVals[level] >= self.lvlVals[self.consoleLvl]:
                if newLine:
                    print(*args, sep='\n')
                else:
                    print(*args)
        except KeyError:
            raise ValueError("level not acceptable value, given '{}' should be {}".format(level, list(Logger.lvlVals.keys())))
        # Set tags
        if self.incTags:
            tags = '[{:17}][{:6}] '.format(self.getTime(), level)
        else:
            tags = ''
        # Get arguments as a string
        if newLine:
            output = ''
            for i in args:
                output += tags + str(i) + '\n'
        else:
            output = tags + ' '.join((str(i) for i in args)) + '\n'
        # Write to log file
        with open(self.logFile, 'at') as f:
            f.write(output)
        return

##### FUNCTIONS #####
def newDir(dirPath):
    """
        Checks if all directories in a path exist and if not makes the missing ones.
        
        
        Parameters
        ----------
        dirPath: string 
            Path to the directory to be created.
        
        Returns
        ----------
        None: none
            None value.
    """
    #List of directories to be created
    makeDirs = []
    checkDir = str(dirPath)
    #Loop until found directory that exists
    while not os.path.exists(checkDir):
        makeDirs.append(checkDir)
        if checkDir.rfind("\\") == -1:
            checkDir =  checkDir[:checkDir.rfind("/")]
        else:
            checkDir =  checkDir[:checkDir.rfind("\\")]
        
    #Loop until dirTree exists
    count = len(makeDirs) - 1
    while not os.path.exists(dirPath):
        if count < 0:
            raise ValueError("Count too low!")
        os.mkdir(makeDirs[count])
        count -= 1
        
    return None
    

##### TEST CODE #####
if __name__ == '__main__':
    timer = TimeTaken()
    log = Logger('test.log', append=True, tags=True)
    log.printOut('Testing', level='debug')
    test = list(range(10))
    log.printOut(*test, level='info', newLine=True)
    log.printOut('Time taken', timer.getTimeTaken())