import math
from EstructuraTrama import EstructuraTrama
from PatronDeColor import PatronDeColor
from Imagen3 import Imagen


class TramaBER:
    def __init__(self,NumTramas,tamanoUtil,numColores,tamanoMatriz):
        self.NumTramas = NumTramas
        self.tamanoUtil = tamanoUtil
        self.BitsPorTrama = int((((tamanoMatriz*tamanoMatriz)-3)*math.log2(numColores))-32) 
        self.numColores = numColores
        self.tamanoMatriz = tamanoMatriz
        self.celdaSincro = 0
        Bytes = numpy.fromfile("textoPruebas.txt", dtype = "uint8")
        self.contenido = numpy.unpackbits(Bytes)
        #print('Bits contenido: ', self.contenido.size)
        #print('Bits por trama*: ',self.BitsPorTrama)
        #print('Número de tramas: ',self.NumTramas)
        
    def generarTramas(self):
        for x in range(self.NumTramas):
            self.celdaSincro = x%2
            cont = self.contenido[(x*self.BitsPorTrama):((x+1)*self.BitsPorTrama)]
            tramaX = EstructuraTrama(self.NumTramas,x+1,self.BitsPorTrama,self.tamanoUtil,cont)
            print(tramaX.getTrama(),tramaX.getTrama().size)
    
        
        

        
