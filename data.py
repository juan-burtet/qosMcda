#!/usr/bin/env python3
class Data:
    
    def __init__(self, name, value=None, normalizedValue=None, weight=1):
        self.name = name
        self.value = value
        self.normalizedValue = normalizedValue
        self.weight = weight

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def setValue(self, value):
        self.value = value

    def setNormalizedValue(self, value):
        self.normalizedValue = value

    def setWeight(self, value):
        self.weight = value