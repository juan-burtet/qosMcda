#!/usr/bin/env python3
from attribute import Attribute

class Service:
    
    attributes = []
    name = None
    wsrf = 0
    mcda = None
    classification = None

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def updateWsrf(self):
        for attribute in self.attributes:
            self.wsrf += attribute.getQuality()

    def updateMcda(self, wsrfMax):
        self.mcda = round((100*self.wsrf)/wsrfMax)

        if (self.mcda > 70):
            self.classification = 1
        elif (self.mcda > 60):
            self.classification = 2
        elif (self.mcda > 50):
            self.classification = 3
        else:
            self.classification = 4

    def getAttributes(self):
        return self.attributes
    
    def getMcda(self):
        return self.mcda
    
    def getClassification(self):
        return self.classification

    def getWsrf(self):
        return self.wsrf
    
    def getName(self):
        return self.name