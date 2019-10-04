# -*- coding: utf-8 -*-
"""
Module containing some Quality of life functions and classes.

Classes
----------
    TimeTaken
        Simple class for measuring the time taken for a program to run and outputting it in a readable way.
    ParamerFile
        Class for handlind parameter files.

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

    def remainingTime(self, remainingLaps, newLap=False):
        """ Returns the remaining time in a readable format when given the number of laps left. """
        avgLap = self.avgLapTime(newLap)
        if avgLap == None:
            return self._readableTime(None)
        # Calculate time left in this lap
        # get absolute value so if this lap is > avgLap it adds time on to time left
        remainingLap = abs(avgLap - (time.time() - self.laps[-1]))
        timeLeft = avgLap * remainingLaps + remainingLap
        return self._readableTime(timeLeft)

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
def newDir(dirPath, number=False, ignoreEmpty=False):
    """
        Checks if all directories in a path exist and if not makes the missing ones.


        Parameters
        ----------
        dirPath: string
            Path to the directory to be created.
        number: boolean
            Whether or not to create a new directory, with a number,
            if dirPath already exists and is not empty.
        ignoreEmpty: boolean
            Whether or not to still create a new directory, with a number,
            if dirPath exists and is empty.

        Returns
        ----------
        info, path: tuple of 2 strings
            Tuple containing a string explaining what newDir has done
            and the path to the directory.
    """
    # Normalise path
    dirPath = os.path.normpath(str(dirPath))
    # Check if full path exists
    if os.path.isdir(dirPath):
        # Check if directory needs numbering
        if number and (len(os.listdir(dirPath)) != 0 or ignoreEmpty):
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

    #List of directories to be created
    makeDirs = []
    checkDir = dirPath
    #Loop until found directory that exists
    while not os.path.exists(checkDir):
        makeDirs.append(checkDir)
        checkDir = checkDir[:checkDir.rfind(os.path.sep)]

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
    test = list(range(10))
    print('Time taken', timer.getTimeTaken())