#!/usr/bin/env python3
class Data:
    
    quality = None
    normalizedValue = None

    def __init__(self, name, maximized=True, value=None, weight=1):
        self.name = name
        self.value = value
        self.weight = weight
        self.maximized = maximized

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setNormalizedValue(self, value):
        self.normalizedValue = value
    
    def getNormalizedValue(self):
        return self.normalizedValue

    def setWeight(self, value):
        self.weight = value

    def setMaximized(self, value):
        self.maximized = value

    def normalize(self, avrg):
        if (self.maximized == True):            
            self.normalizedValue = self.value/float(avrg)
        else:
            self.normalizedValue = avrg/float(self.value)
            
    def setQuality(self, max):
        self.quality = self.normalizedValue*(self.weight/max)
    
    def getQuality(self,):
        return self.quality
    