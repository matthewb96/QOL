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
        self.start = time.time()
        self.laps = [self.start]
        return
    
    def _readableTime(self, timeVal):
        """ Returns a readable formatted string of the given time. """
        # If the timeVal is not a number return ??
        try:
            timeVal = float(timeVal)
        except (TypeError, ValueError) as e:
            return '?? secs.'
        
        if timeVal >= 60:
            timeValSecs = int(timeVal % 60)
            timeValMins = int((timeVal - timeValSecs) / 60)
            if timeValMins >= 60:
                timeValMins = int(timeValMins % 60)
                timeValHrs = int((timeVal - (timeValMins * 60) - timeValSecs) / 3600)
                return "{} hrs, {} mins, {} secs.".format(timeValHrs, timeValMins, timeValSecs)
            else:
                return "{} mins, {} secs.".format(timeValMins, timeValSecs)
        elif timeVal < 1:
            return "< 1 sec."
        else:
            return "{:.0f} secs.".format(timeVal)
        
    def getTimeTaken(self):
        """Returns a readable formatted string of the time taken."""
        #Calc time taken
        timeTaken = round(time.time() - self.start)
        return self._readableTime(timeTaken)
        
    def resetStart(self):
        """Resets the start time and the laps list, returns new start time."""
        self.start = time.time()
        self.laps = [self.start]
        return self.start
    
    def newLap(self):
        """ Adds current time to laps list, returns list. """
        self.laps.append(time.time())
        return self.laps
    
    def avgLapTime(self, newLap=False):
        """ Calculates the average time taken each lap. """
        # Create a newLap if option is True
        if newLap:
            self.newLap()
        # If there is only one value in laps then return None
        if len(self.laps) <= 1:
            return None
        # Get the time taken for each lap
        timeTaken = []
        for i, val in enumerate(self.laps):
            if i == 0:
                continue
            timeTaken.append(val - self.laps[i-1])
        # Calculate average
        return sum(timeTaken)/len(timeTaken)
    
    def getLapTime(self, lapIndex=-1, newLap=False):
        """ Returns the time of a single lap, given by lapIndex, in a readable format. """
        if newLap:
            self.newLap()
        return self._readableTime(self.laps[lapIndex]-self.laps[lapIndex-1])
    
    def remainingTime(self, remainingLaps):
        """ Returns the remaining time in a readable format when given the number of laps left. """
        avgLap = self.avgLapTime()
        if avgLap == None:
            return self._readableTime(None)
        # Calculate time left in this lap
        # get absolute value so if this lap is > avgLap it adds time on to time left
        remainingLap = abs(avgLap - (time.time() - self.laps[-1]))
        timeLeft = avgLap * remainingLaps + remainingLap
        return self._readableTime(timeLeft)

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
        self.checkLevel(level)
        self.consoleLvl = level.upper()
        return
    
    def checkLevel(self, level):
        """Checks the level given is allowed, raises ValueError if it isn't."""
        if level.upper() not in Logger.lvlVals.keys():
            raise ValueError("level not acceptable value, given '{}' should be {}".format(level, list(Logger.lvlVals.keys())))
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
                    Whether or not to put each argument on a new line. Default False.
        """
        self.checkLevel(level)
        # Print if level is greater than console level
        if self.lvlVals[level.upper()] >= self.lvlVals[self.consoleLvl]:
            if newLine:
                print(*args, sep='\n')
            else:
                print(*args)
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

class ParameterFile:
    """ Class that can read and write parameter text files, to be used for various variables within a script. """
    class Parameter:
        """ Class for storing a single parameter. """
        def __init__(self, name, value, typeCheck, description=None):
            # Try to convert value to type
            try:
                if typeCheck in ('int', 'str', 'float'):
                    # Convert string value to built in type
                    self.value = eval(typeCheck + "('{}')".format(value))
                else:
                    # Convert string to non built in type
                    module = __import__(typeCheck[0])
                    func = getattr(module, typeCheck[1])
                    self.value = func(value)
            except (TypeError, ValueError) as e:
                raise TypeError('Parameter is not correct type,' + 
                                'Name: {}, value given: {}, type expected: {}'.format(name, value, typeCheck))
            self.type = typeCheck
            # Set name and description
            self.name = str(name)
            if description == None:
                self.description = ''
            else:
                self.description = str(description)
            return
        
        def __str__(self):
            outStr = 'Name: {}\nValue: {}\nType: {}\nDescription: {}'.format(
                    self.name, self.value, self.type, self.description)
            return outStr
    
    COMMENTS = ['#', '*']
        
    def __init__(self):
        self.parameters = []
        return
    
    def parameterDict(self):
        """ Returns the parameters as a dictionary. """
        paramDict = {}
        for i in self.parameters:
            paramDict[i.name] = i.value
        return paramDict
    
    def getParamIndex(self, name):
        """ Returns the index of the parameter with the given name, None if parameter doesn't exist. """
        paramNames = [i.name for i in self.parameters]
        try:
            return paramNames.index(name)
        except ValueError:
            return None
    
    def addParameter(self, name, value, typeCheck, description=None, overwrite=True):
        """ Adds parameter object to parameters list, overwrites any parameters with the same name. """
        index = self.getParamIndex(name)
        parameter = self.Parameter(name, value, typeCheck, description)
        if index != None and overwrite:
            self.parameters[index] = parameter
        else:
            self.parameters.append(parameter)
        return parameter
    
    def readFile(self, filePath, paramTypes=None):
        """ Reads the parameter text file and loads each parameter, checks parameters if paramTypes dictionary given. """
        with open(filePath, 'rt') as f:
            for line in f:
                line = line.strip()
                # Ignore any comment lines
                if line.startswith(tuple(self.COMMENTS)) or line == '':
                    continue
                # Read parameter
                name, value = line.split('=')
                name = name.strip()
                value = value.strip()
                try:
                    typeCheck = paramTypes[name]
                except (KeyError, TypeError) as e:
                    typeCheck = 'str'
                self.addParameter(name, value, typeCheck)
        return
    
    def writeFile(self, filePath):
        with open(filePath, 'wt') as f:
            for i in self.parameters:
                if i.description != '':
                    f.write('# {}\n'.format(i.description))
                f.write('{} = {}\n'.format(i.name, i.value))
        return
    

##### FUNCTIONS #####
def newDir(dirPath, number=False):
    """
        Checks if all directories in a path exist and if not makes the missing ones.
        
        
        Parameters
        ----------
        dirPath: string 
            Path to the directory to be created.
        number: boolean
            Whether or not to create a new directory, with a number, 
            if dirPath already exists and is not empty.
        
        Returns
        ----------
        info, path: tuple of 2 strings
            Tuple containing a string explaining what newDir has done
            and the path to the directory.
    """
    #List of directories to be created
    makeDirs = []
    checkDir = str(dirPath)
    # Check if full path exists
    if os.path.isdir(dirPath):
        # Check if directory needs numbering
        if number and os.listdir(dirPath) != 0:
            if dirPath.endswith('/') or dirPath.endswith('\\'):
                dirPath = dirPath[:-1] + '_{}' + dirPath[-1]
            else:
                dirPath = dirPath + '_{}'
            count = 1
            newDir = dirPath.format(count)
            while os.path.exists(newDir):
                count += 1
                newDir = dirPath.format(count)
            os.mkdir(newDir)
            return ('New directory created with number {}'.format(count),
                    newDir)
        else:
            return ('Directory already exists.', dirPath)
        
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
        
    return ('Directory tree created.', dirPath)
    

##### TEST CODE #####
if __name__ == '__main__':
    timer = TimeTaken()
    log = Logger('test.log', append=True, tags=True)
    log.printOut('Testing', level='debug')
    test = list(range(10))
    log.printOut(*test, level='info', newLine=True)
    log.printOut('Time taken', timer.getTimeTaken())