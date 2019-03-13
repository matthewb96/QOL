# -*- coding: utf-8 -*-
"""
Module containing some Quality of life functions and classes.
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
    print('Testing')
    print('Time taken', timer.getTimeTaken())