#!/usr/bin/env python3
from data import Data

class Service:
    
    responseTime = None
    availability = None
    throughput = None
    reliability = None
    latency = None
    name = None

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
        