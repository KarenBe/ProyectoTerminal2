from muestraDeColor import muestraDeColor
import numpy as np
import math

class Trama:
    def __init__(self,arregloBits,tamanoMatriz,numColores):
        self.numeroTramas = 0
        self.numeroDeTrama = 0
        self.longitudCU = 0
        self.cargaUtil = 0
        self.Relleno = 0
        self.CRC = 0
        self.tamanoMatriz = tamanoMatriz
        self.arregloBits = arregloBits
        self.numColores = numColores

    def obtenerCampos(self):

        BitsPorTrama = int((((self.tamanoMatriz*self.tamanoMatriz)-3)*math.log2(self.numColores))-32)        
        bitslongitudCU = math.ceil(math.log2(BitsPorTrama))
        BitsPorTrama = BitsPorTrama - bitslongitudCU

        self.numeroTramas = int(''.join(map(str,  self.arregloBits[0:8]                     )),2)
        self.numeroDeTrama = int(''.join(map(str, self.arregloBits[8:16]                    )),2)
        self.longitudCU = int(''.join(map(str,    self.arregloBits[16:16+bitslongitudCU]   )),2)
        self.cargaUtil = self.arregloBits[16+bitslongitudCU : self.longitudCU+16+bitslongitudCU]

        if self.longitudCU != BitsPorTrama:
            #HAY BITS DE RELLENO
            self.Relleno = self.arregloBits[self.longitudCU : BitsPorTrama]
        
        self.CRC = self.arregloBits[BitsPorTrama+self.longitudCU+16:]
        

        
        print("numero de tramas: ", self.numeroTramas)
        print("numero de trama: ",  self.numeroDeTrama)
        print("longitud CU: ",      self.longitudCU)
        print("Carga útil: ",       self.cargaUtil)
        print("Bits de relleno: ",  self.Relleno)
        print("CRC: ",              self.CRC)


