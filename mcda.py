#!/usr/bin/env python3
import csv
from service import Service
from data import Data
import copy
import random

class Mcda:
    responseTimeWeight = 1
    availabilityWeight = 1
    throughputWeight = 1
    reliabilityWeight = 1
    latencyWeight = 1
    
    responseTime = Data('Response Time', weight=responseTimeWeight, maximized=False)
    availability = Data('Availability', weight=availabilityWeight)
    throughput = Data('Throughput', weight=throughputWeight)
    reliability = Data('Reliability', weight=reliabilityWeight)
    latency = Data('Latency', weight=latencyWeight, maximized=False)

    serviceNameColumn = 5
    responseTimeColumn = 0
    availabilityColumn = 1
    throughputColumn = 2
    reliabilityColumn = 3
    latencyColumn = 4

    serviceList=[]
    skipFirstRow = True
    saveToFile = False

    def __init__(self, saveToFile=False):
        self.saveToFile = saveToFile

    def loadFromRandom(self, size):
        
        for x in range(0, size):
            newService = None            
            newService = Service('service-'+str(x), self.responseTime, self.availability, self.throughput, self.reliability, self.latency)

            newService.setResponseTime(random.randint(100, 400))
            newService.setAvailability(random.randint(70, 100))
            newService.setThroughput(random.randint(1, 15))
            newService.setReliability(random.randint(50, 80))
            newService.setLatency(random.randint(1, 200))

            self.serviceList.append(copy.deepcopy(newService))
    

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

    def printResult(self):
        for service in self.getServiceList():
            print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(service.responseTime))
            print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(service.availability))
            print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(service.throughput))
            print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(service.reliability))
            print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(service.latency))

            # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.responseTime))
            # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.availability))
            # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.throughput))
            # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.reliability))
            # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.latency))

    def storeResult(self, fileName="./newData.csv"):
        with open(fileName, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            serviceHeads = []
            
            serviceHeads.insert(self.responseTimeColumn, "Response Time");
            serviceHeads.insert(self.availabilityColumn, "Availability");
            serviceHeads.insert(self.throughputColumn,   "Throughput");
            serviceHeads.insert(self.reliabilityColumn,  "Reliability");
            serviceHeads.insert(self.latencyColumn,      "Latency");
            serviceHeads.insert(self.serviceNameColumn,  "Service Name");
            serviceHeads.insert(len(serviceHeads),   "");
            serviceHeads.insert(len(serviceHeads)+1,   "WSRF");
            serviceHeads.insert(len(serviceHeads)+2,   "MCDA");
            serviceHeads.insert(len(serviceHeads)+3,   "Classification");
            
            writer.writerow(serviceHeads)

            for value in self.getServiceList():
                serviceInfoArr = []

                serviceInfoArr.insert(self.responseTimeColumn, value.getResponseTime().getValue());
                serviceInfoArr.insert(self.availabilityColumn, value.getAvailability().getValue());
                serviceInfoArr.insert(self.throughputColumn,   value.getThroughput().getValue());
                serviceInfoArr.insert(self.reliabilityColumn,  value.getReliability().getValue());
                serviceInfoArr.insert(self.latencyColumn,      value.getLatency().getValue());
                serviceInfoArr.insert(self.serviceNameColumn,  value.getName());

                serviceInfoArr.insert(len(serviceInfoArr),   "");
                serviceInfoArr.insert(len(serviceInfoArr)+1,   "{0:.2f}".format(value.getWsrf()));
                serviceInfoArr.insert(len(serviceInfoArr)+2,   value.getMcda());
                serviceInfoArr.insert(len(serviceInfoArr)+3,   value.getClassification());
                writer.writerow(serviceInfoArr)

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



    def setResponseTimeWeight(self, weight):
        self.responseTimeWeight = weight

    def setAvailabilityWeight(self, weight):
        self.availabilityWeight = weight

    def setThroughputWeight(self, weight):
        self.throughputWeight = weight

    def setReliabilityWeight(self, weight):
        self.reliabilityWeight = weight

    def setLatencyWeight(self, weight):
        self.latencyWeight = weight


    def getServiceList(self):
        return self.serviceList


