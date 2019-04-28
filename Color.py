import cv2
import math
import numpy as np

class Color:
    def __init__(self,celda):
        self.celda = celda

    def itemfreq(self, a):
        items, inv = np.unique(a, return_inverse=True)
        freq = np.bincount(inv)
        return np.array([items, freq]).T

    def colorDominante(self):
        arr = np.float32(self.celda)
        pixels = arr.reshape((-1, 3))

        n_colors = 10
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        quantized = palette[labels.flatten()]
        quantized = quantized.reshape(self.celda.shape)
        dominant_color = palette[np.argmax(self.itemfreq(labels)[:, -1])]    
        return dominant_color.tolist()
