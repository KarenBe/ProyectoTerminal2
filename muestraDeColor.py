import cv2
from Color import Color
import numpy as np
import math

class muestraDeColor:
    def __init__(self,frame,tamanoMatriz,coloresReferencia,numColores):
        self.frame = frame
        self.tamanoMatriz = tamanoMatriz
        self.coloresReferencia = coloresReferencia
        self.numColores = numColores
        self.tamCelda = 20
    
    def color(self, colorRGB,coloresReferencia):
        distanciaMenor = 1000
        for x in range(self.numColores):
            colorR = coloresReferencia[x,0:3]
            distancia = math.sqrt((colorRGB[0] - colorR[0]) ** 2+
                                  (colorRGB[1] - colorR[1]) ** 2+ 
                                  (colorRGB[2] - colorR[2]) ** 2)
            if distancia<distanciaMenor:
                distanciaMenor = distancia
                col = coloresReferencia[x,3]
        return col
    
    def celda(self):
        matriz = self.frame[2*self.tamCelda:(2+self.tamanoMatriz)*self.tamCelda,2*self.tamCelda:(2+self.tamanoMatriz)*self.tamCelda]
        cv2.imshow('',matriz)
        coloresR1 = self.coloresReferencia[0:self.numColores,0:]
        coloresR2 = self.coloresReferencia[self.numColores:2*self.numColores,0:]
        coloresR3 = self.coloresReferencia[2*self.numColores:,0:]
        arregloColores = np.zeros((self.tamanoMatriz*self.tamanoMatriz)-3, np.uint8)
        aux = 0
        img = np.zeros((512,512,3), np.uint8)

        for f in range(self.tamanoMatriz):
            for c in range(self.tamanoMatriz):
                celda = matriz[f*self.tamCelda:(f+1)*self.tamCelda , c*self.tamCelda:(c+1)*self.tamCelda]
                if (f==0 and c==0) or (f==0 and c==self.tamanoMatriz-1) or (f==self.tamanoMatriz-1 and c==self.tamanoMatriz-1):
                    d=1
                else:
                    if f<(self.tamanoMatriz/2)+2 and c<(self.tamanoMatriz/2)+1:
                        colorC = Color(celda)
                        colorCelda = colorC.colorDominante()
                        arregloColores[aux] = self.color(colorCelda,coloresR1)
                        
                    elif f<(self.tamanoMatriz/2)+2 and c>=(self.tamanoMatriz/2)+1:
                        colorC = Color(celda)
                        colorCelda = colorC.colorDominante()
                        arregloColores[aux] = self.color(colorCelda,coloresR1)

                    else:
                        colorC = Color(celda)
                        colorCelda = colorC.colorDominante()
                        arregloColores[aux] = self.color(colorCelda,coloresR1)
                    aux = aux + 1
        return arregloColores
    
    def mapeoaBit(self):
        indice = int(math.log(self.numColores,2))
        arregloBits = np.zeros((),int)
        arregloColores = self.celda()

        if self.numColores == 2:
            bitsporColor = self.arregloColores                

        elif self.numColores == 4:
            for x in range((self.tamanoMatriz*self.tamanoMatriz)-3):
                if arregloColores[x] == 1:
                    a = np.array([[0,0]])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 2:
                    a = np.array([[0,1]])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 3:
                    a = np.array([[1,0]])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                else:
                    a = np.array([[1,1]])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
        
        else:
            for x in range(self.tamanoMatriz*tamanoMatriz):
                if arregloColores[x] == 0:
                    a = np.array([0,0,0])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 1:
                    a = np.array([0,0,1])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 2:
                    a = np.array([0,1,0])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 3:
                    a = np.array([0,1,1])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 4:
                    a = np.array([1,0,0])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 5:
                    a = np.array([1,0,1])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                elif arregloColores[x] == 6:
                    a = np.array([1,1,0])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
                else:
                    a = np.array([1,1,1])
                    arregloBits = np.concatenate((arregloBits,a),axis=None)
        return arregloBits[1:]