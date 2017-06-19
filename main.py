#!/usr/bin/env python3
from mcda import Mcda

mcda = Mcda()
mcda.setServiceNameColumn(5)
mcda.setResponseTimeColumn(0)
mcda.setAvailabilityColumn(1)
mcda.setThroughputColumn(2)
mcda.setReliabilityColumn(3)
mcda.setLatencyColumn(4)
mcda.skipFirstRow(True)

mcda.loadFromCSV('data.csv')

print(mcda.getServiceList()[0].availability)