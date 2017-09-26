#!/usr/bin/env python3

from mcda import Mcda
from attribute import Attribute
import time
import csv

attributeList = []
serviceList = []

attributeList.append(Attribute("Response Time", maximized=True, weight=1, minValue=0, maxValue=100))
attributeList.append(Attribute("Availability", maximized=True, weight=1, minValue=0, maxValue=100))
attributeList.append(Attribute("Throughput", maximized=True, weight=1, minValue=0, maxValue=100))
attributeList.append(Attribute("Reliability", maximized=True, weight=1, minValue=0, maxValue=100))
attributeList.append(Attribute("Latency", maximized=True, weight=1, minValue=0, maxValue=100))

mcda = Mcda(attributeList, serviceList)

with open("results.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    l = [500,1000,5000,50000,500000]
    for num in l:
        writer.writerow([num])
        mcda.loadFromRandom(num)
        #mcda.loadFromCSV('data.csv')

        # start = time.clock()

        # mcda.normalizeData()
        # mcda.calculateQuality()

        # print("sequencial time: "+str(time.clock() - start))
        for thr in range(1, 5):
            
            writer.writerow([thr])            
            resultList = []
            for x in range(0, 9):
                start = time.clock()

                mcda.normalizeDataP(thr)
                mcda.calculateQualityP(thr)

                resultList.append(str(time.clock() - start).replace(".", ","))

            writer.writerow(resultList)


# mcda.storeResult()

# mcda.printResult()