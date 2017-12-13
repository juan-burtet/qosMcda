#!/usr/bin/env python3
import csv
from service import Service
from attribute import Attribute
import copy
import random
from multiprocessing.dummy import Pool as ThreadPool

class Mcda:

    serviceList=[]
    atributeList=[]

    avrgs = []    
    maxes = []

    def __init__(self, serviceList, atributeList=None):
        self.serviceList = serviceList
        if atributeList != None:
            self.atributeList = atributeList
        else:
            self.atributeList = self.serviceList[0].getAttributes()

        self.avrgs = [0]*len(self.atributeList)
        self.maxes = [0]*len(self.atributeList)
    
    def calculateMcda(self):
        wsrfMax = max(service.getWsrf() for service in self.serviceList)

        for service in self.serviceList:
            service.updateMcda(wsrfMax)
    
    def normalizeData(self):
        listSize  = float(len(self.serviceList))
        
        for service in self.serviceList:
            for i, attribute in enumerate(service.getAttributes()):
                self.avrgs[i] += float(attribute.getValue())
                
        for avrg in self.avrgs:
            avrg = float(avrg/listSize)

        for service in self.serviceList:
            for i, attribute in enumerate(service.getAttributes()):
                attribute.normalize(self.avrgs[i])

    def calculateSum(self, service, avrgs):
        # with self.lock:
        for i, attribute in enumerate(service.getAttributes()):
            self.avrgs[i] += float(attribute.getValue())

    def normalizeService(self, service):
        for service in self.serviceList:
            for i, attribute in enumerate(service.getAttributes()):
                attribute.normalize(self.avrgs[i])

    def normalizeDataP(self,thr):
        listSize = len(self.serviceList)

        pool = ThreadPool(thr) 
        pool.map_async(self.calculateSum, self.serviceList)
        pool.close() 
        pool.join() 

        for avrg in self.avrgs:
            avrg = float(avrg/listSize)

        pool = ThreadPool(thr) 
        pool.map_async(self.normalizeService, self.serviceList)
        pool.close() 
        pool.join()

    def calculateQuality(self):
        for service in self.serviceList:
            for i, attribute in enumerate(service.getAttributes()):
                if (attribute.getNormalizedValue() > self.maxes[i]):
                    self.maxes[i] = attribute.getNormalizedValue()

        for service in self.serviceList:
            for i, attribute in enumerate(service.getAttributes()):
                attribute.setQuality(self.maxes[i])
                    
            service.updateWsrf()
        
        self.calculateMcda()

    def serviceMax(self, service):
        # with self.lock:
        for i, attribute in enumerate(service.getAttributes()):
            if (attribute.getNormalizedValue() > self.maxes[i]):
                self.maxes[i] = attribute.getNormalizedValue()

    def qualifyService(self, service):
        for i, attribute in enumerate(service.getAttributes()):
            attribute.setQuality(self.maxes[i])
    
        service.updateWsrf()

    def calculateQualityP(self,thr):
        listSize = len(self.serviceList)

        pool = ThreadPool(thr)
        pool.map_async(self.serviceMax, self.serviceList)
        pool.close() 
        pool.join() 

        pool = ThreadPool(thr)        
        pool.map_async(self.qualifyService, self.serviceList)
        pool.close() 
        pool.join()

        self.calculateMcda()

    def printResult(self):
        for service in self.getServiceList():
            for i, attribute in enumerate(service.getAttributes()):
                print(service.getName()+" (Classification="+str(service.getClassification())+"): "+str(attribute))

    def storeResult(self, fileName="./mcdaResult.csv"):
        with open(fileName, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            serviceHeads = []

            for attribute in self.serviceList[0].getAttributes():
                serviceHeads.append(attribute.getName())

            serviceHeads.append("")
            serviceHeads.append("WSRF")
            serviceHeads.append("MCDA")
            serviceHeads.append("Classification")
            
            writer.writerow(serviceHeads)

            for service in self.getServiceList():
                serviceInfoArr = []

                for attribute in service.getAttributes():
                    serviceInfoArr.append(attribute.getValue())

                serviceInfoArr.append("")
                serviceInfoArr.append("{0:.2f}".format(service.getWsrf()))
                serviceInfoArr.append(service.getMcda())
                serviceInfoArr.append(service.getClassification())

                writer.writerow(serviceInfoArr)

    def getServiceList(self):
        return self.serviceList