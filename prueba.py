import cv2
from coloresReferencia import coloresReferencia 
from muestraDeColor import muestraDeColor
from Trama import Trama
import crc16

tamCelda = 20
tamMatriz = 16
numColores = 8

image = cv2.imread('16.png')
imagen = coloresReferencia(image,tamMatriz,numColores)

coloresR = imagen.obtenerColoresReferencia()
matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)
bits = matriz.mapeoaBit()
trama = Trama(bits,tamMatriz,numColores)

trama.obtenerCampos()

if trama.tramaValida == True:
    print("valida")
else:
    print("invalida")

#print("arreglo bits: ", bits , bits.size)


cv2.waitKey(0)
cv2.destroyAllWindows()