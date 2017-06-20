#!/usr/bin/env python3
import csv
from service import Service
from data import Data
import copy

class Mcda:    
    
    responseTime = Data('Response Time', weight=1, maximized=False)
    availability = Data('Availability', weight=1)
    throughput = Data('Throughput', weight=1)
    reliability = Data('Reliability', weight=1)
    latency = Data('Latency', weight=1, maximized=False)

    serviceNameColumn = 5
    responseTimeColumn = 0
    availabilityColumn = 1
    throughputColumn = 2
    reliabilityColumn = 3
    latencyColumn = 4

    serviceList=[]
    skipFirstRow = True

    def loadFromCSV(self, file='data.csv'):
            
        with open(file, "rb") as f:
            reader = csv.reader(f)

            if (self.skipFirstRow):
                next(reader)

            for row in reader:
                newService = None
                if row[0] in (None, ""):
                    break
                else:                    
                    newService = Service(row[self.serviceNameColumn], self.responseTime, self.availability, self.throughput, self.reliability, self.latency)

                    newService.setResponseTime(float(row[self.responseTimeColumn].replace(',','.')))
                    newService.setAvailability(float(row[self.availabilityColumn].replace(',','.')))
                    newService.setThroughput(float(row[self.throughputColumn].replace(',','.')))
                    newService.setReliability(float(row[self.reliabilityColumn].replace(',','.')))
                    newService.setLatency(float(row[self.latencyColumn].replace(',','.')))

                    self.serviceList.append(copy.deepcopy(newService))
    
    def calculateMcda(self):
        wsrfMax = max(service.getWsrf() for service in self.serviceList)

        for service in self.serviceList:
            service.updateMcda(wsrfMax)

    def normalizeData(self):
        rtAvrg = sum(float(service.responseTime.getValue()) for service in self.serviceList)/float(len(self.serviceList))
        aAvrg = sum(float(service.availability.getValue()) for service in self.serviceList)/float(len(self.serviceList))
        tAvrg = sum(float(service.throughput.getValue()) for service in self.serviceList)/float(len(self.serviceList))
        rAvrg = sum(float(service.reliability.getValue()) for service in self.serviceList)/float(len(self.serviceList))
        lAvrg = sum(float(service.latency.getValue()) for service in self.serviceList)/float(len(self.serviceList))
        for service in self.serviceList:
            service.responseTime.normalize(rtAvrg)
            service.availability.normalize(aAvrg)
            service.throughput.normalize(tAvrg)
            service.reliability.normalize(rAvrg)
            service.latency.normalize(lAvrg)

    def calculateQuality(self):
        rtMax = max(service.responseTime.getNormalizedValue() for service in self.serviceList)
        aMax = max(service.availability.getNormalizedValue() for service in self.serviceList)
        tMax = max(service.throughput.getNormalizedValue() for service in self.serviceList)
        rMax = max(service.reliability.getNormalizedValue() for service in self.serviceList)
        lMax = max(service.latency.getNormalizedValue() for service in self.serviceList)

        for service in self.serviceList:
            service.responseTime.setQuality(rtMax)
            service.availability.setQuality(aMax)
            service.throughput.setQuality(tMax)
            service.reliability.setQuality(rMax)
            service.latency.setQuality(lMax)
        
            service.updateWsrf()
        
        self.calculateMcda()

    def skipFirstRow(self, value):
        self.skipFirstRow = value

    def setServiceNameColumn(self, column):
        self.serviceNameColumn = column

    def setResponseTimeColumn(self, column):
        self.responseTimeColumn = column

    def setAvailabilityColumn(self, column):
        self.availabilityColumn = column

    def setThroughputColumn(self, column):
        self.throughputColumn = column

    def setReliabilityColumn(self, column):
        self.reliabilityColumn = column

    def setLatencyColumn(self, column):
        self.latencyColumn = column

    def getServiceList(self):
        return self.serviceList


