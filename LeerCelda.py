import cv2
import math
import numpy as np

def itemfreq(a):
    items, inv = np.unique(a, return_inverse=True)
    freq = np.bincount(inv)
    return np.array([items, freq]).T

def colorDominante(celda):
    arr = np.float32(celda)
    pixels = arr.reshape((-1, 3))

    n_colors = 10
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    palette = np.uint8(centroids)
    quantized = palette[labels.flatten()]
    quantized = quantized.reshape(celda.shape)
    dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
    return dominant_color.tolist()
    
def CeldasSincronizacion(image):
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
        colorD = colorDominante(celda)
        print(colorD)
        cv2.rectangle(image,((x-1)*tamCelda,(y-1)*tamCelda),(x*tamCelda,y*tamCelda),colorD,-1)
    cv2.imshow('color dominante',image)
    cv2.waitKey(0)


image = cv2.imread('tam16.jpg')
coloresReferencia = CeldasSincronizacion(image)

cv2.waitKey(0)
cv2.destroyAllWindows()