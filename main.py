#!/usr/bin/env python3
from mcda import Mcda

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

mcda.loadFromRandom(200000)
# mcda.loadFromCSV('data.csv')

mcda.normalizeData()
mcda.calculateQuality()

mcda.storeResult()

# mcda.printResult()