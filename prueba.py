import cv2
from coloresReferencia import coloresReferencia 
from muestraDeColor import muestraDeColor
from Trama import Trama
import crc16
from rotarImagen import rotarImagen

tamCelda = 20
tamMatriz = 8
numColores = 4

image = cv2.imread('Nuevo16-1.png')

r = rotarImagen(image,tamMatriz,numColores)

cv2.imshow("original",image)
cv2.imshow("rotada",r.rotar())

cv2.waitKey(0)
cv2.destroyAllWindows()



#imagen = coloresReferencia(image,tamMatriz,numColores)

#coloresR = imagen.obtenerColoresReferencia()
#matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)
#bits = matriz.mapeoaBit()
#trama = Trama(bits,tamMatriz,numColores)

#trama.obtenerCampos()

#if trama.tramaValida == True:
#    print("valida")
#else:
#    print("invalida")

#print("arreglo bits: ", bits , bits.size)


