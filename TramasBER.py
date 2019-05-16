import math
from EstructuraTrama import EstructuraTrama
import numpy


class TramaBER:
    def __init__(self,NumTramas,numColores,tamanoMatriz):
        self.NumTramas = NumTramas
        self.BitsPorTrama = int((((tamanoMatriz*tamanoMatriz)-3)*math.log2(numColores))-32) 
        self.numColores = numColores
        self.tamanoMatriz = tamanoMatriz
        self.celdaSincro = 0
        f = open('textoPruebas.txt', 'r')
        Bytes = numpy.fromfile(f, dtype = "uint8")
        print(Bytes)
        self.contenido = numpy.unpackbits(Bytes)
        #print('Bits contenido: ', self.contenido.size)
        #print('Bits por trama*: ',self.BitsPorTrama)
        #print('Número de tramas: ',self.NumTramas)
        
    def generarTramas(self):
        for x in range(self.NumTramas):
            self.celdaSincro = x%2
            tamanoUtil = math.ceil(math.log2(self.BitsPorTrama))
            cont = self.contenido[(x*self.BitsPorTrama):((x+1)*self.BitsPorTrama)]
            tramaX = EstructuraTrama(self.NumTramas,x+1,self.BitsPorTrama,tamanoUtil,cont)
            print(tramaX.getTrama(),tramaX.getTrama().size)
    
        
        

        
