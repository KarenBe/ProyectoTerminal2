import cv2
import math
import numpy as np
from Color import Color

class CeldaSincronizacion:
    def LeerCeldas(image):
        tamMatrix=16
        celdaPatron = tamMatrix + 4
        width=np.size(image, 0)
        tamCelda = math.ceil(width/celdaPatron)


        for m in range (3):
            if m==0:
                x=3
                y=3
            elif m==1:
                x=tamMatrix+2
                y=tamMatrix+2
            else:
                x=tamMatrix+2
                y=3

            celda = image[(y-1)*tamCelda:y*tamCelda, (x-1)*tamCelda: x*tamCelda]
            colorD = Color(celda)
            vColor= colorD.colorDominante()
            print(vColor)
            cv2.rectangle(image,((x-1)*tamCelda,(y-1)*tamCelda),(x*tamCelda,y*tamCelda),(0,255,0),-1)
            
        cv2.imshow('color dominante',image)
        cv2.waitKey(0)


#image = cv2.imread('tam16.jpg')
#coloresReferencia = CeldaSincronizacion.LeerCeldas(image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()