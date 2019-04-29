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
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
            else:
                celda = self.frame[0:self.tamCelda, ((x*2)+1)*self.tamCelda: ((x*2)+2)*self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
        return coloresR

    def CRIzquierda(self):
        img = np.zeros((512,512,3), np.uint8)
        coloresR = np.zeros((self.numColores,3),int)
        #Colores de referencia
        for x in range (self.numColores):
            if x == self.numColores-1:
                celda = self.frame[(x*2)*self.tamCelda: ((x*2)+1)*self.tamCelda , (self.tamanoMatriz+3)*self.tamCelda:(self.tamanoMatriz+4)*self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
            else:
                celda = self.frame[((x*2)+1)*self.tamCelda: ((x*2)+2)*self.tamCelda , (self.tamanoMatriz+3)*self.tamCelda:(self.tamanoMatriz+4)*self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
        return coloresR

    def CRInferior(self):
        img = np.zeros((512,512,3), np.uint8)
        coloresR = np.zeros((self.numColores,3),int)

        #Colores de referencia
        inicio = ((self.tamanoMatriz+4)-(2*(self.numColores-1)))*self.tamCelda

        for x in range (self.numColores):
            if x == self.numColores-1:
                celda = self.frame[(self.tamanoMatriz+3)*self.tamCelda: (self.tamanoMatriz+4)*self.tamCelda , inicio+((self.numColores-1)*2*self.tamCelda)-self.tamCelda:]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
            else:
                celda = self.frame[(self.tamanoMatriz+3)*self.tamCelda:(self.tamanoMatriz+4)*self.tamCelda , inicio+(2*(x)*self.tamCelda):(inicio+(2*(x+1)*self.tamCelda))-self.tamCelda]
                colorD = Color(celda)
                coloresR[x,:] = colorD.colorDominante()
                #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
                #cv2.imshow('color dominante',img)
                #cv2.imshow('celda', celda)
                #cv2.waitKey(0)
        return coloresR

    def obtenerColoresReferencia(self):
        sup = self.CRSuperior()
        izq = self.CRIzquierda()
        inf = self.CRInferior()

        cr = np.concatenate((sup,izq,inf),axis=0)

        return cr

