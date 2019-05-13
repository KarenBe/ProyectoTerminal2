import cv2
from Color import Color
import numpy as np
import math

class rotarImagen():
    def __init__(self,image,tamMatriz,numColores):
        self.image = image
        self.tamMatriz = tamMatriz
        self.numColores = numColores
        self.tamCelda = 20
    
    def rotar(self):
        colores = np.ones((4,3))

        inicio = int(self.tamMatriz-(self.numColores/2)) + 1
        celda1 = self.image[0:self.tamCelda,2*self.tamCelda:3*self.tamCelda]
        color1 = Color(celda1)
        colores[0,:] = color1.colorDominante()

        celda2 = self.image[2*self.tamCelda:3*self.tamCelda,(self.tamMatriz+3)*self.tamCelda:(self.tamMatriz+4)*self.tamCelda]
        color2 = Color(celda2)
        colores[1,:] = color2.colorDominante()

        celda3 = self.image[(self.tamMatriz+3)*self.tamCelda:(self.tamMatriz+4)*self.tamCelda , -3*self.tamCelda:-2*self.tamCelda]
        color3 = Color(celda3)
        colores[2,:] = color3.colorDominante()

        celda4 = self.image[-3*self.tamCelda:-2*self.tamCelda,0:self.tamCelda]
        color4 = Color(celda4)
        colores[3,:] = color4.colorDominante()

        #Calcular distancias
        negro = [0,0,0]
        distanciaMenor = 10000
        for i in range(4):
            color = colores[i,:]
            distancia = math.sqrt((color[0] - negro[0]) ** 2+
                                  (color[1] - negro[1]) ** 2+ 
                                  (color[2] - negro[2]) ** 2)
            if distancia<distanciaMenor:
                distanciaMenor = distancia
                indice = i
        indicadores = np.ones((4),dtype = int)
        indicadores[indice] = 0
        
        if np.array_equal(indicadores,np.array([0,1,1,1],dtype = int)):
            imageRotada = self.rotateImage(self.image,90)
        elif np.array_equal(indicadores,np.array([1,0,1,1],dtype = int)):
            imageRotada = self.rotateImage(self.image,180)
        elif np.array_equal(indicadores,np.array([1,1,0,1],dtype = int)):
            imageRotada = self.rotateImage(self.image,-90)
        else:
            imageRotada = self.image
        return imageRotada
    

    def rotateImage(self,image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
