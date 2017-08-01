#!/usr/bin/env python3
from mcda import Mcda
import time

mcda = Mcda(True)
mcda.setServiceNameColumn(5)
mcda.setResponseTimeColumn(0)
mcda.setAvailabilityColumn(1)
mcda.setThroughputColumn(2)
mcda.setReliabilityColumn(3)
mcda.setLatencyColumn(4)
# mcda.skipFirstRow(True)

mcda.setResponseTimeWeight(1)
mcda.setAvailabilityWeight(1)
mcda.setThroughputWeight(1)
mcda.setReliabilityWeight(1)
mcda.setLatencyWeight(1)

mcda.loadFromRandom(50000)
#mcda.loadFromCSV('data.csv')

start = time.clock()

mcda.normalizeData()
mcda.calculateQuality()

print("sequencial time: "+str(time.clock() - start))
start = time.clock()

mcda.normalizeDataP()
mcda.calculateQualityP()

print("thread time: "+str(time.clock() - start))

mcda.storeResult()

# mcda.printResult()