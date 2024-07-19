## Script


import logging

HOUR = 3600
DAY = 24 * HOUR


class TimeConstraints(object):

    def __init__(self, duration=0, repeatInterval=0, startTime=0):
        duration = int(duration)
        repeatInterval = int(repeatInterval)
        startTime = int(startTime)

        self.valid = False
        if duration == 0 and repeatInterval == 0 and startTime == 0:
            self.valid = True
        else:
            if repeatInterval <= 0 or repeatInterval > DAY \
                    or DAY % repeatInterval != 0 \
                    or repeatInterval < duration \
                    or startTime < 0 or startTime > DAY \
                    or duration < 0 or duration > DAY:
                
                logging.warning("Bad init values for TimeConstraints: " +
                                "duration: %d  repeatInterval: %d  " +
                                "startTime: %d",
                                duration, repeatInterval, startTime)
                self.valid = False
                duration = 0
                repeatInterval = 0
                startTime = 0
            else:
                self.valid = True
        
        self.duration = duration
        self.repeatInterval = repeatInterval
        self.startTime = startTime
        
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if not self.isValid():
            return "<Invalid>"
        elif not self.anyConstraints():
            return "<NoConstraints>"
        else:
            return "[s=" + str(self.startTime // HOUR) + "h, i=" + \
                   str(self.repeatInterval // HOUR) + "h, d=" + \
                   str(self.duration // HOUR) + "h]"
                   
    def __eq__(self, other):
        if not isinstance(other, TimeConstraints):
            return False
        if self.isValid() != other.isValid():
            return False
        if self.duration != other.duration:
            return False
        if self.repeatInterval != other.repeatInterval:
            return False
        return (self.startTime == other.startTime)
    
    def __ne__(self, other):
        return (not self.__eq__(other))
    
    def anyConstraints(self):
        return (self.duration != 0)
    
    def isValid(self):
        return self.valid

    def getDuration(self):
        return self.duration

    def getRepeatInterval(self):
        return self.repeatInterval

    def getStartTime(self):
        return self.startTime
