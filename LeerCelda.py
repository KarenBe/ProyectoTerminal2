import cv2
import math
import numpy as np
from Color import Color

class CeldaSincronizacion:
    def __init__(self,tamMatriz):
        self.tamMatriz = int(tamMatriz)

    def LeerCeldas(self,image):
        celdaPatron = self.tamMatriz + 4
        width=np.size(image, 0)
        tamCelda = math.ceil(width/celdaPatron)
        coloresCS = coloresR = np.zeros((3,3),int)  #colores de las celdas de sincronización
        
        for m in range (3):
            if m==0:
                x=3
                y=3
            elif m==1:
                x=self.tamMatriz+2
                y=self.tamMatriz+2
            else:
                x=self.tamMatriz+2
                y=3

            celda = image[(y-1)*tamCelda:y*tamCelda, (x-1)*tamCelda: x*tamCelda]
            colorD = Color(celda)
            vColor= colorD.colorDominante()
            coloresCS[m,:] = colorD.colorDominante()
            #cv2.rectangle(image,((x-1)*tamCelda,(y-1)*tamCelda),(x*tamCelda,y*tamCelda),(0,255,0),-1)
        
        return coloresCS    
        #cv2.imshow('color dominante',image)
        #cv2.waitKey(0)


#image = cv2.imread('tam16.jpg')
#CS=CeldaSincronizacion(16)
#coloresReferencia = CS.LeerCeldas(image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()