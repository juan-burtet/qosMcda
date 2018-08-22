#!/usr/bin/env python3

from mcda import Mcda
from attribute import Attribute
from datasetGenerator import DatasetLoader
import time
import csv

# Lista de Atributos + Lista de Serviços
attributeList = []
serviceList = []

# Adiciona os Atributos
attributeList.append(Attribute("Response Time", maximized=False, weight=1, minValue=100, maxValue=400))
attributeList.append(Attribute("Availability", maximized=True, weight=1, minValue=1, maxValue=100))
attributeList.append(Attribute("Throughput", maximized=True, weight=1, minValue=1, maxValue=30))
attributeList.append(Attribute("Reliability", maximized=True, weight=1, minValue=1, maxValue=100))
attributeList.append(Attribute("Latency", maximized=False, weight=1, minValue=1, maxValue=300))
attributeList.append(Attribute("Successability", maximized=True, weight=1, minValue=1, maxValue=100))
attributeList.append(Attribute("Agility", maximized=True, weight=1, minValue=1, maxValue=100))

# Manda os atributos para o criador de dataset
dataset = DatasetLoader(attributeList)

# Pega o tempo do sistema
startDataset = time.clock()

# Gera um dataset de tamanho 500.000
serviceList = dataset.generateRandom(500000)

# Imprime o tempo levado para gerar o Dataset
print("Tempo de geracao de dataset: " + str(time.clock() - startDataset) + "s\n")

# Pega o tempo do sistema
start = time.clock()

# Faz o calculo MCDA do Dataset gerado
mcda = Mcda(serviceList, attributeList)
mcda.normalizeData()
mcda.calculateQuality()

# Imprime o tempo levado para o calculo MCDA do dataset
print("Tempo de classificacao: "+str(time.clock() - start)+"s\n")

# Guarda os resultados em um arquivo csv
mcda.storeResult()
print("Os resultados foram salvos em: mcdaResult.csv\n\n")
