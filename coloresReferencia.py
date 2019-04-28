import cv2
import math
import numpy as np
from Color import Color

class coloresReferencia:
    def __init__(self,frame,tamanoMatriz,numColores):
        self.frame = frame
        self.tamanoMatriz = tamanoMatriz
        self.numColores = numColores
        self.tamCelda = 20
        
    def CRSuperior(self):
        img = np.zeros((512,512,3), np.uint8)
        coloresR = np.zeros((self.numColores,3),int)

        #Colores de referencia
        for x in range (self.numColores):
            if x == self.numColores-1:
                celda = self.frame[0:self.tamCelda, (x*2)*self.tamCelda: ((x*2)+1)*self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
            else:
                celda = self.frame[0:self.tamCelda, ((x*2)+1)*self.tamCelda: ((x*2)+2)*self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
        return coloresR

    def CRIzquierda(self):
        img = np.zeros((512,512,3), np.uint8)

        tamMatriz = 16 + 4
        numColores = 8
        tamCelda = math.ceil(300/tamMatriz)
        coloresReferencia = np.zeros((numColores,3),int)

        #Colores de referencia
        for x in range (numColores):
            if x == coloresReferencia-1:
                celda = self.frame[(x*2)*tamCelda: ((x*2)+1)*tamCelda , (tamMatriz-1)*tamCelda:tamMatriz*tamCelda]
                colorD = colorDominante(celda)
                coloresReferencia[x,:] = colorD
                cv2.rectangle(img,(30,0),(50,50),colorD,-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
            else:
                celda = self.frame[((x*2)+1)*tamCelda: ((x*2)+2)*tamCelda , (tamMatriz-1)*tamCelda:tamMatriz*tamCelda]
                colorD = colorDominante(celda)
                coloresReferencia[x,:] = colorD
                cv2.rectangle(img,(30,0),(50,50),colorD,-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
        return coloresReferencia

    def CRInferior(self):
        img = np.zeros((512,512,3), np.uint8)

        tamMatriz = 16 + 4
        numColores = 8
        tamCelda = math.ceil(300/tamMatriz)
        coloresReferencia = np.zeros((numColores,3),int)

        #Colores de referencia
        for x in range (numColores):
            if x == numColores-1:
                celda = self.frame[((x*2)+1)*tamCelda: ((x*2)+2)*tamCelda , 19*tamCelda:20*tamCelda]
                colorD = colorDominante(celda)
                coloresReferencia[x,:] = colorD
                cv2.rectangle(img,(30,0),(50,50),colorD,-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
            else:
                celda = self.frame[((x*2)+1)*tamCelda: ((x*2)+2)*tamCelda , 19*tamCelda:20*tamCelda]
                colorD = colorDominante(celda)
                coloresReferencia[x,:] = colorD
                cv2.rectangle(img,(30,0),(50,50),colorD,-1)
                cv2.imshow('color dominante',img)
                cv2.imshow('celda', celda)
                cv2.waitKey(0)
        return coloresReferencia
