#!/usr/bin/env python3
import csv
from service import Service
from attribute import Attribute
import random
import copy

class datasetLoader:

    attributeList={}
    serviceList=[]

    def __init__(self, atrList):
        self.attributeList = atrList

    def generateRandom(self, size):
        for x in range(0, size):
            newService = None            
            
            for attribute in self.attributeList:
                attribute.setRandomValue()

            newService = Service('service-'+str(x), self.attributeList)

            self.serviceList.append(copy.deepcopy(newService))

        return self.serviceList

    # def loadFromCSV(self, file='data.csv'):
            
    #     with open(file, "rb") as f:
    #         reader = csv.reader(f)

    #         if (self.skipFirstRow):
    #             next(reader)

    #         for row in reader:
    #             newService = None
    #             if row[0] in (None, ""):
    #                 break
    #             else:                    
    #                 newService = Service(row[self.serviceNameColumn], self.responseTime, self.availability, self.throughput, self.reliability, self.latency)

    #                 newService.setResponseTime(float(row[self.responseTimeColumn].replace(',','.')))
    #                 newService.setAvailability(float(row[self.availabilityColumn].replace(',','.')))
    #                 newService.setThroughput(float(row[self.throughputColumn].replace(',','.')))
    #                 newService.setReliability(float(row[self.reliabilityColumn].replace(',','.')))
    #                 newService.setLatency(float(row[self.latencyColumn].replace(',','.')))

    #                 self.serviceList.append(copy.deepcopy(newService))

    def storeDataset(self, fileName="./newDataset.csv"):
        with open(fileName, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            serviceHeads = []

            for attribute in self.attributeList:
                serviceHeads.append(attribute.getName());
                # serviceHeads.insert(self.availabilityColumn, "Availability");
            
            writer.writerow(serviceHeads)

            for service in self.serviceList:
                serviceInfoArr = []

                for attribute in service.getAttributes():
                    serviceInfoArr.append(attribute.getValue());
                serviceInfoArr.append(service.getName());

                writer.writerow(serviceInfoArr)