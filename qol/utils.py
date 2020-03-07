"""
    Module containing any miscallaneous utility functions and classes.
"""

##### IMPORTS #####
# Standard imports
import time

##### CLASSES #####
class TimeTaken:
    """
        Simple class for measuring the time taken for a program to run and
        outputting it in a readable way.
    """

    def __init__(self):
        """ Sets start to currect time when class is instanciated. """
        self.start = time.time()
        self.laps = [self.start]
        return

    def _readableTime(self, timeVal):
        """ Returns a readable formatted string of the given time.

        Parameters
        ----------
        timeVal: int or float
            Time taken in seconds.

        Returns
        -------
        timeTaken: str
            `timeVal` formatted into hours, minutes and seconds.

        Note
        ----
        If `timeVal` is less than 1 seconds then '< 1 sec.' is returned. If `timeVal`
        is not a number then '?? secs.' is returned.
        """
        # If the timeVal is not a number return ??
        try:
            timeVal = float(timeVal)
        except (TypeError, ValueError):
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
        """ Gets a readable formatted string of the time taken.

        .. todo::
            Change timeTaken to a property of the class.

        Returns
        -------
        timeTaken: str
            `timeVal` formatted into hours, minutes and seconds.
        """
        #Calc time taken
        timeTaken = round(time.time() - self.start)
        return self._readableTime(timeTaken)

    def resetStart(self):
        """ Resets the start time and the laps list.

        Returns
        -------
        start: time.time
            The new start time.
        """
        self.start = time.time()
        self.laps = [self.start]
        return self.start

    def newLap(self):
        """ Adds current time to laps list.

        Returns
        -------
        laps: list
            List of all the lap times.
        """
        self.laps.append(time.time())
        return self.laps

    def avgLapTime(self, newLap=False):
        """ Calculates the average time taken each lap.

        Parameters
        ----------
        newLap: bool, optional
            Whether to create a new lap (True) before calculating
            the average or not (False, default).

        Returns
        -------
        avgTime: float
            The average time taken for a lap, in seconds.
        """
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
        """ Gets the time of a single lap, given by lapIndex, in a readable format.

        Parameters
        ----------
        lapIndex: int, optional
            The index number for which lap to get the time for, defaults to -1
            to get the last lap.
        newLap: bool, optional
            Whether to create a new lap (True) before getting the
            lap time or not (False, default).

        Returns
        -------
        lapTime: str
            The lap time of lap with index `lapIndex` in a readable format.
        """
        if newLap:
            self.newLap()
        return self._readableTime(self.laps[lapIndex]-self.laps[lapIndex-1])

    def remainingTime(self, remainingLaps, newLap=False):
        """ Gets the remaining time in a readable format when given the number of laps left.

        Parameters
        ----------
        remainingLaps: int
            The number of laps remaining.
        newLap: bool, optional
            Whether to create a new lap (True) before getting the
            remaining time or not (False, default).

        Returns
        -------
        remainingTime: str
            The time it would take to complete `remainingLaps` based on the average
            lap time.
        """
        avgLap = self.avgLapTime(newLap)
        if avgLap is None:
            return self._readableTime(None)
        # Calculate time left in this lap
        # get absolute value so if this lap is > avgLap it adds time on to time left
        remainingLap = abs(avgLap - (time.time() - self.laps[-1]))
        timeLeft = avgLap * remainingLaps + remainingLap
        return self._readableTime(timeLeft)
