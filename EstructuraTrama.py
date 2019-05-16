import numpy as np
import math
import crc16
import random

f = open('tramas.txt','w')
class EstructuraTrama:
        def __init__(self,numeroTramas,numeroTrama,BitsPorTrama,longitudCU,cargaUtil):
                
            self.numeroTramas = self.aBinario(numeroTramas,8)
            self.numeroTrama = self.aBinario(numeroTrama,8)
            self.cargaUtil = cargaUtil
            self.longitudCU = self.aBinario(cargaUtil.size,longitudCU)
            self.bitsRelleno = BitsPorTrama-cargaUtil.size
            self.CRC = self.aBinario(crc16.crc16xmodem(self.cargaUtil),16)
            
            f = open('tramas.txt','a')
            f.write('\n\n*****************************************************************\n')
            f.write('Tramas: ' + str(numeroTramas) + str(self.numeroTramas) + 'Longitud:' + str(self.numeroTramas.size) + '\n')
            f.write('Numero de trama: ' + str(numeroTrama) + str(self.numeroTrama) + 'Longitud:' + str(self.numeroTrama.size) +'\n')
            f.write('Longitud carga util: ' + str(self.longitudCU.size) + str(self.longitudCU) + '\n')
            f.write('Carga util: ' + str(self.cargaUtil.size) + str(type(self.cargaUtil)) + str(type(self.cargaUtil[2])) + '\n')
            f.write(str(self.cargaUtil) + '\n')
            f.write('Relleno: ' + str(self.bitsRelleno) + '\n')
            f.write('CRC: ' + str(crc16.crc16xmodem(self.cargaUtil)) + str(self.CRC) + str(type(self.CRC)) + str(self.CRC.dtype)+'\n\n')
            f.close()
            print("abierto")
        def aBinario(self,numero,nbits):
            nb = '{0:0'+str(nbits)+'b}'
            nb = nb.format(numero)
            nb = list(nb)
            nb = np.array(nb)
            nb = nb.astype(int)
            return nb

        def getTrama(self):
                if self.bitsRelleno > 0:
                        relleno = [random.randint(0,1) for _ in range(self.bitsRelleno)]
                        relleno = np.array(relleno)

                        trama = np.concatenate((self.numeroTramas,
                                                self.numeroTrama,
                                                self.longitudCU,
                                                self.cargaUtil,
                                                relleno,
                                                self.CRC), axis=None)
                else:
                        trama = np.concatenate((self.numeroTramas,
                                                self.numeroTrama,
                                                self.longitudCU,
                                                self.cargaUtil,
                                                self.CRC), axis=None)
                    
                return trama
                    
                    
            
            
