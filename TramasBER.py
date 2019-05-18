import math
from EstructuraTrama import EstructuraTrama
import numpy

f = open('prueba.txt', 'r')
Bytes = numpy.fromfile(f, dtype = "uint8")
class TramaBER:
    def __init__(self,NumTramas,numColores,tamanoMatriz):
        self.NumTramas = NumTramas
        self.BitsPorTrama = int((((tamanoMatriz*tamanoMatriz)-3)*math.log2(numColores))-32)
        self.numColores = numColores
        self.tamanoMatriz = tamanoMatriz
        self.celdaSincro = 0
        self.tamanoUtil = math.ceil(math.log2(self.BitsPorTrama))
        self.contenido = numpy.unpackbits(Bytes)
        self.BitsPorTrama = self.BitsPorTrama - self.tamanoUtil
        self.tramas = []

        
    def generarTramas(self):
        for x in range(self.NumTramas):
            self.celdaSincro = x%2
            cont = self.contenido[(x*self.BitsPorTrama):((x+1)*self.BitsPorTrama)]
            tramaX = EstructuraTrama(self.NumTramas,x+1,self.BitsPorTrama,self.tamanoUtil,cont)
            self.tramas.append(tramaX.getTrama())
            
    
    def compararTrama(self,numTrama,arraybits):
        res=self.tramas[numTrama-1]-arraybits
        incorrectos=sum(res!=0)
        BER=incorrectos/len(arraybits)
        print("# Bits incorrectos:",incorrectos)
        print("BER de la trama: ",BER)
        print("Bits correcto: ",self.tramas[numTrama-1])
        print("Bits recibidos: ",arraybits)
        return BER
        

        
