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
             celda = self.frame[0:self.tamCelda, ((x))*self.tamCelda: ((x)+1)*self.tamCelda]
             colorD = Color(celda)
             coloresR[x,0:3] = colorD.colorDominante()
             #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
             #cv2.imshow('color dominante',img)
             #cv2.imshow('celda', celda)
             #cv2.waitKey(0)
        if self.numColores == 2:
            c = np.array([[1,0]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        elif self.numColores == 4:
            c = np.array([[1,2,3,4]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        else:
            c = np.array([[1,0,2,3,4,5,6,7]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        return cr

    def CRIzquierda(self):
        img = np.zeros((512,512,3), np.uint8)
        coloresR = np.zeros((self.numColores,3),int)
        #Colores de referencia
        for x in range (self.numColores):
             celda = self.frame[(x)*self.tamCelda: ((x)+1)*self.tamCelda , (self.tamanoMatriz+3)*self.tamCelda:(self.tamanoMatriz+4)*self.tamCelda]
             colorD = Color(celda)
             coloresR[x,:3] = colorD.colorDominante()
             #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
             #cv2.imshow('color dominante',img)
             #cv2.imshow('celda', celda)
             #cv2.waitKey(0)
        if self.numColores == 2:
            c = np.array([[1,0]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        elif self.numColores == 4:
            c = np.array([[1,2,3,4]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        else:
            c = np.array([[1,0,2,3,4,5,6,7]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        return cr

    def CRInferior(self):
        img = np.zeros((512,512,3), np.uint8)
        coloresR = np.zeros((self.numColores,3),int)

        #Colores de referencia
        inicio = int(self.tamanoMatriz-(self.numColores/2))

        for x in range (self.numColores):
             celda = self.frame[(self.tamanoMatriz+3)*self.tamCelda:(self.tamanoMatriz+4)*self.tamCelda , (inicio+x)*self.tamCelda : (x+1+inicio)*self.tamCelda]
             colorD = Color(celda)
             coloresR[x,:3] = colorD.colorDominante()
             #cv2.rectangle(img,(30,0),(50,50),colorD.colorDominante(),-1)
             #cv2.imshow('color dominante',img)
             #cv2.imshow('celda', celda)
             #cv2.waitKey(0)
        if self.numColores == 2:
            c = np.array([[0,1]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        elif self.numColores == 4:
            c = np.array([[2,3,4,1]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        else:
            c = np.array([[0,2,3,4,5,6,7,1]])
            cr = np.concatenate((coloresR,c.T),axis=1)
        return cr

    def obtenerColoresReferencia(self):
        sup = self.CRSuperior()
        izq = self.CRIzquierda()
        inf = self.CRInferior()

        cr = np.concatenate((sup,izq,inf),axis=0)
        return cr

