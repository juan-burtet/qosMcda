#!/usr/bin/env python3
import random

# Classe que representa um Atributo
# Um Atributo possui:
#	- Nome
#	- Valor
#	- Peso
#	- Boolean se deve ser Maximizado
#	- Valor Minimo
#	- Valor Maximo
#	- Qualidade do Atributo
# - Valor Normalizado
class Attribute:
    
		# Construtor do Attribute
		# @param name - Nome do Atributo
		# @param maximized - Indica se o Atributo deve ser maximizado 
		# @param value - Valor do Atributo
		# @param weight - Peso do Atributo
		# @param minValue - Valor minimo do Atributo
		#	@param maxValue - Valor maximo do Atributo
    def __init__(self, name, maximized=True, value=None, weight=1, minValue=0, maxValue=100):
        
        # Nome do Atributo
        self.name = name
        # Valor do Atributo
        self.value = value
        # Peso do Atributo
        self.weight = weight
        # Indica se o Atributo deve ser maximizado
        self.maximized = maximized
        # Valor minimo do Atributo
        self.minValue=minValue
        # Valor maximo do Atributo
        self.maxValue=maxValue
        # Qualidade do Atributo
        self.quality = None
        # Valor Normalizado do Atributo
        self.normalizedValue = None

    # Saida str
    # @return str
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    # Saida repr
    # @return repr
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # Retorna o atributo em formado Dict
    # @return atributo em formado Dict
    def toDict(self): 
        return {self.name:self.value}

    # Adiciona um valor ao atributo
    # @param value - valor
    def setValue(self, value):
        self.value = round(value, 2)
    
    # Adiciona um valor aleatório ao atributo
    def setRandomValue(self):
        self.value = round(random.uniform(self.minValue, self.maxValue), 2)
		
		# Retorna o nome do Atributo
		# @return nome do atributo
    def getName(self):
        return self.name
		
		# Retorna o valor do Atributo
		# @return valor do atributo
    def getValue(self):
        return self.value
		
		# Retorna o valor minimo do Atributo
		# @return valor minimo do atributo
    def getMinValue(self):
        return self.minValue
		
		# Retorna o valor maximo do Atributo
		# @return valor maximo do atributo
    def getMaxValue(self):
        return self.maxValue
		
		# Atualiza o valor minimo do atributo
		# @param value - valor minimo
    def setMinValue(self, value):
        self.minValue = value
		
		# Atualiza o valor maximo do atributo
		# @param value - valor maximo
    def setMaxValue(self, value):
        self.maxValue = value
		
		# Atualiza o valor normalizado do atributo
		# @param value - Valor Normalizado
    def setNormalizedValue(self, value):
        self.normalizedValue = value
    
    # Retorna o valor normalizado
    # @return valor normalizado
    def getNormalizedValue(self):
        return self.normalizedValue

    # Atualiza o peso do atributo
    # @param value - peso do atributo
    def setWeight(self, value):
        self.weight = value

    # Atualiza se o atributo é maximizado
    # @param value - Boolean se deve ser maximizado
    def setMaximized(self, value):
        self.maximized = value

		# Normaliza o valor do Atributo
		# @param avrg- - Média dos valores dos atributos
    def normalize(self, avrg):
    
    		# Se o valor precisa ser maximizado, 
    		# ValorNormalizado = valor/media
        if (self.maximized == True):            
            self.normalizedValue = self.value/float(avrg)
        # Se o valor não precisa ser maximizado,
        # ValorNormalizado = media/valor
        else:
            self.normalizedValue = avrg/float(self.value)
            
    # Adiciona a qualidade do Atributo
    # @param maxv - Maior valor normalizado desse Atributo
    # @return Qualidade do Serviço
    def setQuality(self, maxv):
    		
    		# Qualidade = (ValorNormalizado)*(Peso/MaiorValorNormalizado)
        self.quality = float(self.normalizedValue)*(float(self.weight/maxv))
        return self.quality
    
    # Retorna a Qualidade do Atributo
    # @return Qualidade do Atributo
    def getQuality(self):
        return self.quality
    
