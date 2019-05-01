import cv2
import math
import numpy as np

class Sincronizacion:
    def __init__(self,ColorAnterior,ColorNuevo):
        self.ColorAnterior=ColorAnterior
        self.ColorNuevo=ColorNuevo
        print('Color Ant: '+format(self.ColorAnterior))
        print('Color nue: '+format(self.ColorNuevo))
    
    def CompararCeldas(self):
        distanciaMenor = 70

        distancia = math.sqrt((self.ColorAnterior[0][0] - self.ColorNuevo[0][0]) ** 2+
                                  (self.ColorAnterior[0][1] - self.ColorNuevo[0][1]) ** 2+ 
                                  (self.ColorAnterior[0][2] - self.ColorNuevo[0][2]) ** 2)
        print("Distancia: "+format(distancia))
        if distancia<distanciaMenor:
            return 1
        else:
            return 0
        