# -*- coding: utf-8 -*-
"""
Module containing some Quality of life functions and classes.
"""
##### IMPORTS #####
import os

##### CLASSES #####

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
    print('Testing')