#!/usr/bin/env python3
from attribute import Attribute

# Classe que representa um Serviço
# Um Serviço possui:
#	- Nome
#	- Lista de Atributos
# - Valor WSRF do Serviço
#	- Valor MCDA do Serviço
#	- Classificação do Serviço
class Service:
    
    # Construtor do Serviço
    # @param name - Nome do Serviço
    # @param attributes - Lista de Atributos do Serviço
    def __init__(self, name, attributes):
        
        # Nome do Serviço
        self.name = name							
        # Lista de Atributos
        self.attributes = attributes	
        # Valor do wsrf = 0
        self.wsrf = 0									
        # Valor do MCDA = None
        self.mcda = None										
        # Classificação do Serviço = None
        self.classification = None					
		
		# Saida str
		# @return Nome do Serviço
    def __str__(self):
        return self.name
    
    # Saida repr
    # @return Nome do Serviço
    def __repr__(self):
        return self.name

    # Atualiza o valor Wsrf
    def updateWsrf(self):
    
    		# Soma os valores de Qualidade dos Atributos
        for attribute in self.attributes:
            self.wsrf += attribute.getQuality()
		
		# Atualiza o valor MCDA e a Classificação do serviço
		# @param WsrfMax - Wsrf Máximo de todos os serviços
    def updateMcda(self, wsrfMax):
        
        # Calcula o valor MCDA
        self.mcda = round((100*self.wsrf)/wsrfMax)
				
				# Se o mcda for acima de 70, classificação = 1
        if (self.mcda > 70):
            self.classification = 1
        # Se o mcda for acima de 60, classificação = 2
        elif (self.mcda > 60):
            self.classification = 2
        # Se o mcda for acima de 50, classificação = 3
        elif (self.mcda > 50):
            self.classification = 3
        # Se o mcda for abaixo ou igual a 50, classificação = 4
        else:
            self.classification = 4
    
    # Transforma o serviço em Dict
    # @return Retorna em formato Dict
    def toDict(self):
        d = dict()
        d.update({"name":self.name})
        for attribute in self.attributes:
            d.update(attribute.toDict())

        return d
		
		# Retorna os atributos do serviço
		# @return Lista de Atributos
    def getAttributes(self):
        return self.attributes
    
    # Get especified attribute by name
    # def getAttributes(self, name):
    #     return filter(lambda x: x.getName() == name, self.attributes)            
            
    # Retorna o valor MCDA do serviço
    # @return Valor MCDA do serviço
    def getMcda(self):
        return self.mcda
    
    # Retorna a Classificação do serviço
    # @return Classificação do Serviço
    def getClassification(self):
        return self.classification

		# Retorna o Wsrf do serviço
		# @return Valor wsrf do Serviço
    def getWsrf(self):
        return self.wsrf
    
    # Retorna o nome do serviço
    # @return Nome do Serviço
    def getName(self):
        return self.name
