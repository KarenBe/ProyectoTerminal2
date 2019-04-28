import cv2
from coloresReferencia import coloresReferencia 

image = cv2.imread('img8.png')
imagen = coloresReferencia(image,8,2)
coloresR = imagen.CRSuperior()
print(coloresR)

cv2.imshow('original', image)
cv2.waitKey(0)
cv2.destroyAllWindows()