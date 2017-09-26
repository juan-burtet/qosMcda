#!/usr/bin/env python3

from mcda import Mcda
from attribute import Attribute
from datasetGenerator import DatasetLoader
import time
import csv

attributeList = []
serviceList = []

attributeList.append(Attribute("Response Time", maximized=False, weight=1, minValue=100, maxValue=400))
attributeList.append(Attribute("Availability", maximized=True, weight=1, minValue=70, maxValue=100))
attributeList.append(Attribute("Throughput", maximized=True, weight=1, minValue=1, maxValue=15))
attributeList.append(Attribute("Reliability", maximized=True, weight=1, minValue=50, maxValue=80))
attributeList.append(Attribute("Latency", maximized=False, weight=1, minValue=1, maxValue=200))

dataset = DatasetLoader(attributeList)
serviceList = dataset.generateRandom(1000)

start = time.clock()

mcda = Mcda(serviceList, attributeList)

mcda.normalizeData()
mcda.calculateQuality()

print("Tempo de classificacao: "+str(time.clock() - start)+"s\n")

mcda.storeResult()
print("Os resultados foram salvos em: mcdaResult.csv\n\n")

# mcda.printResult()

# teste paralelo
# with open("results.csv", "wb") as csv_file:
#     writer = csv.writer(csv_file, delimiter=',')
#     l = [500,1000,5000,50000,500000]
#     for num in l:
#         writer.writerow([num])
#         mcda.loadFromRandom(num)
#         #mcda.loadFromCSV('data.csv')

#         # start = time.clock()

#         # mcda.normalizeData()
#         # mcda.calculateQuality()

#         # print("sequencial time: "+str(time.clock() - start))
#         for thr in range(1, 5):
            
#             writer.writerow([thr])            
#             resultList = []
#             for x in range(0, 9):
#                 start = time.clock()

#                 mcda.normalizeDataP(thr)
#                 mcda.calculateQualityP(thr)

#                 resultList.append(str(time.clock() - start).replace(".", ","))

#             writer.writerow(resultList)


# mcda.storeResult()

# mcda.printResult()