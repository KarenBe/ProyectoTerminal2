import cv2
from coloresReferencia import coloresReferencia 
from muestraDeColor import muestraDeColor
from Trama import Trama

tamCelda = 20
tamMatriz = 12
numColores = 4

image = cv2.imread('img12.png')
imagen = coloresReferencia(image,tamMatriz,numColores)

coloresR = imagen.obtenerColoresReferencia()
cv2.imshow('original', image)

matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)
trama = Trama(matriz.mapeoaBit(),tamMatriz,numColores)
trama.obtenerCampos()

print("arreglo bits: ", matriz.mapeoaBit())


cv2.waitKey(0)
cv2.destroyAllWindows()