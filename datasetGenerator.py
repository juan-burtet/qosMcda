#!/usr/bin/env python3
import csv
from service import Service
from attribute import Attribute
import random
import copy

class DatasetLoader:


    def __init__(self, atrList):
        self.attributeList = atrList
        self.serviceList=[]
        self.qtServices = 0

    def toDict(self):
        l = []

        for service in self.serviceList:
            l.append(service.toDict())        

        return l
		
	# É adicionado n atributos random a lista de serviços
	# @param size - Quantos atributos serem gerados
	# @return retorna lista de serviços completa
    def generateRandom(self, size):
        
        # Percorre pela quantidade de serviços a serem gerados
        for _ in range(size):
            newService = None            
            
            # Gera valores random para todos os atributos
            for attribute in self.attributeList:
                attribute.setRandomValue()
						
			# Novo serviço random criado
            newService = Service('service-' + str(self.qtServices), self.attributeList)
            # Aumenta a quantidade de serviços
            self.qtServices += 1
						
			# Adiciona o novo serviço na lista de serviços
            self.serviceList.append(copy.deepcopy(newService))
				
				# Retorna a lista de Serviços
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

    # Guarda o dataset em um arquivo .csv
    # @param fileName - Nome do arquivo csv
    def storeDataset(self, fileName="./newDataset.csv"):
        
        # abre o arquivo para escrita
        with open(fileName, "w") as csv_file:
            
            
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
