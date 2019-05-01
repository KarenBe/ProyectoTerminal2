from muestraDeColor import muestraDeColor
import numpy as np
import math
import crc16

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
        self.longitudCU = int(''.join(map(str,    self.arregloBits[16:16+bitslongitudCU]    )),2)
        self.cargaUtil = self.arregloBits[16+bitslongitudCU : self.longitudCU+16+bitslongitudCU]
        self.CRC = int(''.join(map(str,           self.arregloBits[-16:]                    )),2)
        if self.longitudCU != BitsPorTrama:
            #HAY BITS DE RELLENO
            self.Relleno = self.arregloBits[self.longitudCU : BitsPorTrama]
        
        print(self.cargaUtil.shape)
        calculoCRC = crc16.crc16xmodem(self.cargaUtil)

        print(self.frombits(self.cargaUtil))
        
        print("numero de tramas: ", self.numeroTramas)
        print("numero de trama: ",  self.numeroDeTrama)
        print("longitud CU: ",      self.longitudCU)
        print("Carga útil: ",       self.cargaUtil)
        print("Texto recuperado: ", self.frombits(self.cargaUtil))

        print("Bits de relleno: ",  self.Relleno)
        print("CRC calculado: ",    self.CRC)
        print("CRC: ",              self.CRC)

    def frombits(self,bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

