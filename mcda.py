#!/usr/bin/env python3
import csv
from service import Service
from data import Data

class Mcda:    
    
    responseTime = Data('Response Time')
    availability = Data('Availability')
    throughput = Data('Throughput')
    reliability = Data('Reliability')
    latency = Data('Latency')

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
                if row[0] in (None, ""):
                    break
                else:                    
                    newService = Service(row[self.serviceNameColumn], self.responseTime, self.availability, self.throughput, self.reliability, self.latency)

                    newService.setResponseTime(row[self.responseTimeColumn])
                    newService.setAvailability(row[self.availabilityColumn])
                    newService.setThroughput(row[self.throughputColumn])
                    newService.setReliability(row[self.reliabilityColumn])
                    newService.setLatency(row[self.latencyColumn])

                    self.serviceList.append(newService)
            # next(reader)
            # for i in range(10):
            #     vet = reader.next()

            #     matrixData.append(vet[0:5])

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


