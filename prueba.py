import cv2
from coloresReferencia import coloresReferencia 
from muestraDeColor import muestraDeColor
from Trama import Trama
import crc16
from rotarImagen import rotarImagen

tamCelda = 20
tamMatriz = 16
numColores = 8

image = cv2.imread('Nuevo16.png')

#r = rotarImagen(image,tamMatriz,numColores)
#cv2.imshow("original",image)
#cv2.imshow("rotada",r.rotar())
#cv2.waitKey(0)
#cv2.destroyAllWindows()

imagen = coloresReferencia(image,tamMatriz,numColores)
coloresR = imagen.obtenerColoresReferencia()

matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)

bits = matriz.indicadores()
trama = Trama(bits,tamMatriz,numColores)
trama.obtenerIndicadores()

#print(trama.numeroDeTrama)

#if trama.tramaValida == True:
#    print("valida")
#else:
#    print("invalida")

#print("arreglo bits: ", bits , bits.size)


