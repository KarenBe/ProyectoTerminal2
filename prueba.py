import cv2
from coloresReferencia import coloresReferencia 
from pruebaCeldas import muestraDeColor

tamCelda = 20
tamMatriz = 12
numColores = 4

image = cv2.imread('img12.png')
imagen = coloresReferencia(image,tamMatriz,numColores)

coloresR = imagen.obtenerColoresReferencia()
print("colores referencia: ",coloresR)
cv2.imshow('original', image)

matriz = muestraDeColor(image,tamMatriz,coloresR,numColores)
matriz.celda()


cv2.waitKey(0)
cv2.destroyAllWindows()