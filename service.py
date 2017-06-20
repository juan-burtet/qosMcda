#!/usr/bin/env python3
from data import Data

class Service:
    
    responseTime = None
    availability = None
    throughput = None
    reliability = None
    latency = None
    name = None
    wsrf = None
    mcda = None
    classification = None

    def __init__(self, name, responseTime, availability, throughput, reliability, latency):
        self.name = name
        self.responseTime = responseTime
        self.availability = availability
        self.throughput = throughput
        self.reliability = reliability
        self.latency = latency

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def updateWsrf(self):
        self.wsrf = self.responseTime.getQuality() + self.availability.getQuality() + self.throughput.getQuality() + self.reliability.getQuality() + self.latency.getQuality()

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
    
    def getMcda(self):
        return self.mcda
    
    def getClassification(self):
        return self.classification

    def getWsrf(self):
        return self.wsrf
    
    def getName(self):
        return self.name

    def setResponseTime(self, value):
        self.responseTime.setValue(value)
        
    def setAvailability(self, value):
        self.availability.setValue(value)
        
    def setThroughput(self, value):
        self.throughput.setValue(value)
        
    def setReliability(self, value):
        self.reliability.setValue(value)
        
    def setLatency(self, value):
        self.latency.setValue(value)

        

    def setNormalizedResponseTime(self, value):
        self.responseTime.setNormalizedValue(value)
        
    def setNormalizedAvailability(self, value):
        self.availability.setNormalizedValue(value)
        
    def setNormalizedThroughput(self, value):
        self.throughput.setNormalizedValue(value)
        
    def setNormalizedReliability(self, value):
        self.reliability.setNormalizedValue(value)
        
    def setNormalizedLatency(self, value):
        self.latency.setNormalizedValue(value)
        