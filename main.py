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

mcda.setResponseTimeWeight(1)
mcda.setAvailabilityWeight(1)
mcda.setThroughputWeight(1)
mcda.setReliabilityWeight(1)
mcda.setLatencyWeight(1)

mcda.loadFromCSV('data.csv')

mcda.normalizeData()
mcda.calculateQuality()

for service in mcda.getServiceList():
    print(service.getName()+" (Class="+str(service.getClassification())+"): "+str(service.responseTime))
    print(service.getName()+" (Class="+str(service.getClassification())+"): "+str(service.availability))
    print(service.getName()+" (Class="+str(service.getClassification())+"): "+str(service.throughput))
    print(service.getName()+" (Class="+str(service.getClassification())+"): "+str(service.reliability))
    print(service.getName()+" (Class="+str(service.getClassification())+"): "+str(service.latency))

    # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.responseTime))
    # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.availability))
    # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.throughput))
    # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.reliability))
    # print(service.getName()+" ("+str(service.getWsrf())+":"+str(service.getMcda())+":"+str(service.getClassification())+"): "+str(service.latency))