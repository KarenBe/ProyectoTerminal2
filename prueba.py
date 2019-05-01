import cv2
from coloresReferencia import coloresReferencia 
from muestraDeColor import muestraDeColor
from Trama import Trama
import crc16

tamCelda = 20
tamMatriz = 16
numColores = 8

image = cv2.imread('Imagen0.png')
imagen = coloresReferencia(image,tamMatriz,numColores)

coloresR = imagen.obtenerColoresReferencia()
print("Colores referencia: ", coloresR)
cv2.imshow('original', image)

matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)
trama = Trama(matriz.mapeoaBit(),tamMatriz,numColores)
trama.obtenerCampos()

print("arreglo bits: ", matriz.mapeoaBit(),matriz.mapeoaBit().size)


cv2.waitKey(0)
cv2.destroyAllWindows()