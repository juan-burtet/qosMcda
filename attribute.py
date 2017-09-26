#!/usr/bin/env python3
import random
class Attribute:
    
    quality = None
    normalizedValue = None

    def __init__(self, name, maximized=True, value=None, weight=1, minValue=0, maxValue=100):
        self.name = name
        self.value = value
        self.weight = weight
        self.maximized = maximized
        self.minValue=min
        self.maxValue=max

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def setValue(self, value):
        self.value = value
    
    def setRandomValue(self, value):
        self.value = random.randint(self.minValue, self.maxValue)

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getMinValue(self):
        return self.minValue

    def getMaxValue(self):
        return self.maxValue

    def setMinValue(self, value):
        self.minValue = value

    def setMaxValue(self, value):
        self.maxValue = value

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
            
    def setQuality(self, maxv):
        self.quality = float(self.normalizedValue)*(float(self.weight/maxv))
        return self.quality
    
    def getQuality(self,):
        return self.quality
    