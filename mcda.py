#!/usr/bin/env python3
import csv
from service import Service
from data import Data
from threadWithReturn import threadWithReturn
import copy
import random
import threading as t
import itertools    
from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import Process, RawValue, Lock

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

    lock = Lock()

    rtAvrg = 0
    aAvrg = 0
    tAvrg = 0
    rAvrg = 0
    lAvrg = 0
    
    rtMax = 0
    aMax = 0
    tMax = 0
    rMax = 0
    lMax = 0

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
        rtAvrg = 0
        aAvrg = 0
        tAvrg = 0
        rAvrg = 0
        lAvrg = 0

        listSize  = float(len(self.serviceList))

        for service in self.serviceList:
            rtAvrg += float(service.responseTime.getValue())
            aAvrg += float(service.availability.getValue())
            tAvrg += float(service.throughput.getValue())
            rAvrg += float(service.reliability.getValue())
            lAvrg += float(service.latency.getValue())

        rtAvrg = float(rtAvrg/listSize)
        aAvrg = float(aAvrg/listSize)
        tAvrg = float(tAvrg/listSize)
        rAvrg = float(rAvrg/listSize)
        lAvrg = float(lAvrg/listSize)

        for service in self.serviceList:
            service.responseTime.normalize(rtAvrg)
            service.availability.normalize(aAvrg)
            service.throughput.normalize(tAvrg)
            service.reliability.normalize(rAvrg)
            service.latency.normalize(lAvrg)

    def calculateSum(self, service):
        with self.lock:
            self.rtAvrg += float(service.responseTime.getValue())
            self.aAvrg += float(service.availability.getValue())
            self.tAvrg += float(service.throughput.getValue())
            self.rAvrg += float(service.reliability.getValue())
            self.lAvrg += float(service.latency.getValue())
    
    def normalizeService(self, service):
        service.responseTime.normalize(self.rtAvrg)
        service.availability.normalize(self.aAvrg)
        service.throughput.normalize(self.tAvrg)
        service.reliability.normalize(self.rAvrg)
        service.latency.normalize(self.lAvrg)

    def normalizeDataP(self):
        self.rtAvrg = 0
        self.aAvrg = 0
        self.tAvrg = 0
        self.rAvrg = 0
        self.lAvrg = 0

        listSize = len(self.serviceList)
        # ranges = listSize/4

        pool = ThreadPool(4) 

        pool.map_async(self.calculateSum, self.serviceList[:listSize/2])
        pool.map_async(self.calculateSum, self.serviceList[listSize/2:])

        pool.close() 
        pool.join() 

        self.rtAvrg = self.rtAvrg/listSize
        self.aAvrg = self.aAvrg/listSize
        self.tAvrg = self.tAvrg/listSize
        self.rAvrg = self.rAvrg/listSize
        self.lAvrg = self.lAvrg/listSize

        pool = ThreadPool(4) 
        
        pool.map_async(self.normalizeService, self.serviceList[:listSize/2])
        pool.map_async(self.normalizeService, self.serviceList[listSize/2:])

        pool.close() 
        pool.join()

        # listSize  = float(len(self.serviceList))
        # t1 = threadWithReturn(target=self.avgServiceThroughput, args=(self.serviceList,))
        # t2 = threadWithReturn(target=self.avgServiceResponseTime, args=(self.serviceList,))
        # t3 = threadWithReturn(target=self.avgServiceAvailability, args=(self.serviceList,))
        # t4 = threadWithReturn(target=self.avgServiceReliability, args=(self.serviceList,))
        # t5 = threadWithReturn(target=self.avgServiceLatency, args=(self.serviceList,))
        
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
        
        # rtAvrg = t1.join()
        # aAvrg = t2.join()
        # tAvrg = t3.join()
        # rAvrg = t4.join()
        # lAvrg = t5.join()

        # for service in self.serviceList:
        #     service.responseTime.normalize(rtAvrg)
        #     service.availability.normalize(aAvrg)
        #     service.throughput.normalize(tAvrg)
        #     service.reliability.normalize(rAvrg)
        #     service.latency.normalize(lAvrg)

    def calculateQuality(self):
        for service in self.serviceList:
            if (service.responseTime.getNormalizedValue() > self.rtMax):
                self.rtMax = service.responseTime.getNormalizedValue()
            if (service.availability.getNormalizedValue() > self.aMax):
                self.aMax = service.availability.getNormalizedValue()
            if (service.throughput.getNormalizedValue() > self.tMax):
                self.tMax = service.throughput.getNormalizedValue()
            if (service.reliability.getNormalizedValue() > self.rMax):
                self.rMax = service.reliability.getNormalizedValue()
            if (service.latency.getNormalizedValue() > self.lMax):
                self.lMax = service.latency.getNormalizedValue()

        for service in self.serviceList:
            service.responseTime.setQuality(self.rtMax)
            service.availability.setQuality(self.aMax)
            service.throughput.setQuality(self.tMax)
            service.reliability.setQuality(self.rMax)
            service.latency.setQuality(self.lMax)
        
            service.updateWsrf()
        
        self.calculateMcda()

    def serviceMax(self, service):
        with self.lock:
            if (service.responseTime.getNormalizedValue() > self.rtMax):
                self.rtMax = service.responseTime.getNormalizedValue()
            if (service.availability.getNormalizedValue() > self.aMax):
                self.aMax = service.availability.getNormalizedValue()
            if (service.throughput.getNormalizedValue() > self.tMax):
                self.tMax = service.throughput.getNormalizedValue()
            if (service.reliability.getNormalizedValue() > self.rMax):
                self.rMax = service.reliability.getNormalizedValue()
            if (service.latency.getNormalizedValue() > self.lMax):
                self.lMax = service.latency.getNormalizedValue()

    def qualifyService(self, service):
        service.responseTime.setQuality(self.rtMax)
        service.availability.setQuality(self.aMax)
        service.throughput.setQuality(self.tMax)
        service.reliability.setQuality(self.rMax)
        service.latency.setQuality(self.lMax)
    
        service.updateWsrf()

    def calculateQualityP(self):
        self.rtMax = 0
        self.aMax = 0
        self.tMax = 0
        self.rMax = 0
        self.lMax = 0

        listSize = len(self.serviceList)
        # ranges = listSize/4

        pool = ThreadPool(4) 

        pool.map_async(self.serviceMax, self.serviceList[:listSize/2])
        pool.map_async(self.serviceMax, self.serviceList[listSize/2:])

        pool.close() 
        pool.join() 

        pool = ThreadPool(4) 
        
        pool.map_async(self.qualifyService, self.serviceList[:listSize/2])
        pool.map_async(self.qualifyService, self.serviceList[listSize/2:])

        pool.close() 
        pool.join()

        self.calculateMcda()
        # t1 = threadWithReturn(target=self.maxServiceThroughput, args=(self.serviceList,))
        # t2 = threadWithReturn(target=self.maxServiceResponseTime, args=(self.serviceList,))
        # t3 = threadWithReturn(target=self.maxServiceAvailability, args=(self.serviceList,))
        # t4 = threadWithReturn(target=self.maxServiceReliability, args=(self.serviceList,))
        # t5 = threadWithReturn(target=self.maxServiceLatency, args=(self.serviceList,))
        
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
        
        # rtMax = t1.join()
        # aMax = t2.join()
        # tMax = t3.join()
        # rMax = t4.join()
        # lMax = t5.join()

        # for service in self.serviceList:
        #     service.responseTime.setQuality(rtMax)
        #     service.availability.setQuality(aMax)
        #     service.throughput.setQuality(tMax)
        #     service.reliability.setQuality(rMax)
        #     service.latency.setQuality(lMax)
        
        #     service.updateWsrf()
        
        # self.calculateMcda()

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


