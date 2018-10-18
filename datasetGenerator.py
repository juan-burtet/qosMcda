#!/usr/bin/env python3
import csv
from service import Service
from attribute import Attribute
import random
import copy

# Classe usada pra gerar um Dataset
# Um DatasetLoader possui:
#   - Uma lista de atributos
#   - Uma lista de serviços
#   - A quantidade de serviços
class DatasetLoader:

    # Construtor do DatasetLoader
    # @param atrList - lista de atributos
    def __init__(self, atrList):

        # Lista de atributos
        self.attributeList = atrList
        # Lista de serviços
        self.serviceList = []
        # Quantidade de Serviços
        self.qtServices = 0

    # Retorna os serviços em formato Dict
    # @return serviços em formato dict
    def toDict(self):
        l = []
        
        # passa por todos os serviços
        for service in self.serviceList:
            l.append(service.toDict())        
        
        # retorna a lista em formato dict
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

    # Guarda o dataset em um arquivo .csv
    # @param fileName - Nome do arquivo csv
    def storeDataset(self, fileName="./newDataset.csv"):
        
        # abre o arquivo para escrita
        with open(fileName, "w") as csv_file:
            
            # escritor do csv
            writer = csv.writer(csv_file, delimiter=',')
            
            # Escreve o cabeçalho no csv
            serviceHeads = []
            for attribute in self.attributeList:
                serviceHeads.append(attribute.getName());
            writer.writerow(serviceHeads)

            # Escreve todos os serviços
            for service in self.serviceList:
                serviceInfoArr = []

                for attribute in service.getAttributes():
                    serviceInfoArr.append(attribute.getValue());
                serviceInfoArr.append(service.getName());

                writer.writerow(serviceInfoArr)
