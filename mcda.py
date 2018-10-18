#!/usr/bin/env python3
import csv
from service import Service
from attribute import Attribute
import copy
import random
from multiprocessing.dummy import Pool as ThreadPool

class Mcda:

  
    # Construtor do MCDA
    # @param serviceList - Lista de serviço
    # @param atributeList - Lista de Atributos
    def __init__(self, serviceList, atributeList=None):
        
        # Lista de Serviços
        self.serviceList = serviceList
        # Lista de atributos
        self.atributeList = atributeList

        # Se a lista de atributos for vazia, pega a lista dos serviços
        if self.atributeList == None:
            self.atributeList = self.serviceList[0].getAttributes()

        # Vetor de médias de cada atributo
        self.avrgs = [0]*len(self.atributeList)
        # Vetor de máximos de cada atributo
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

    # 
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

    # Imprime o Resultado MCDA
    def printResult(self):
        
        # Passa por todos os Serviços
        for service in self.getServiceList():
            # passa pelos atributos de todos os serviços
            for i, attribute in enumerate(service.getAttributes()):
                # Imprime (Nome do Serviço + Classificação + atributos
                print(service.getName() + " (Classification=" + str(service.getClassification()) + "): " + str(attribute))
		
	# Escreve o Resultado MCDA em um arquivo .csv
	# @param fileName - Nome do arquivo
    def storeResult(self, fileName="./mcdaResult.csv"):
        
        # Abre o arquivo para escrita como csv
        with open(fileName, "w") as csv_file:
            
			# Começa a escrita no arquivo            
            writer = csv.writer(csv_file, delimiter=',')
            
            # Cabeçalho pega o nome dos atributos
            serviceHeads = []
            for attribute in self.serviceList[0].getAttributes():
                serviceHeads.append(attribute.getName())
						
			# Cabeçalho adiciona 'WSRF', 'MCDA' e 'Classificação'
            serviceHeads.append("WSRF")
            serviceHeads.append("MCDA")
            serviceHeads.append("Classification")
            
            # Escreve a linha
            writer.writerow(serviceHeads)
						
			# Passa por todos os serviços
            for service in self.getServiceList():
                serviceInfoArr = []

                # Pega os valores dos atributos
                for attribute in service.getAttributes():
                    serviceInfoArr.append(attribute.getValue())
								
				# pega os valores de WSRF, MCDA e Classificação
                serviceInfoArr.append("{0:.2f}".format(service.getWsrf()))
                serviceInfoArr.append(service.getMcda())
                serviceInfoArr.append(service.getClassification())
								
				# escreve a linha
                writer.writerow(serviceInfoArr)

    # Retorna a lista de Serviços
    # @return lista de serviços
    def getServiceList(self):
        return self.serviceList
