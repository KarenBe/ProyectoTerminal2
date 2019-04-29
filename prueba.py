import cv2
from coloresReferencia import coloresReferencia 

image = cv2.imread('img14.png')
imagen = coloresReferencia(image,14,2)
coloresR = imagen.obtenerColoresReferencia()
print(coloresR)

cv2.imshow('original', image)
cv2.waitKey(0)
cv2.destroyAllWindows()