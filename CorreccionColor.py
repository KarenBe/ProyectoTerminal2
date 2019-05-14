import cv2 
import numpy as np 
from PIL import Image, ImageTk

im_gray = cv2.imread("Nuevo16-22.png",cv2.IMREAD_COLOR)
#hsv = cv2.applyColorMap(im_gray, cv2.COLORMAP_HOT)
#hsv = cv2.cvtColor(im_gray, cv2.COLOR_BGR2HSV)
#hsv=cv2.cvtColor(im_gray,cv2.COLORMAP_SPRING)

#hsv = cv2.cvtColor(im_gray, cv2.COLOR_BGR2HSV) 
#cv2.imshow("Im agn",hsv)
lower_red = np.array([208,234,231]) 
upper_red = np.array([220,237,233]) 
mask = cv2.inRange(im_gray, lower_red, upper_red) 
res = cv2.bitwise_and(im_gray,im_gray, mask= mask)  

#img = Image.fromarray(im_gray)
#imgtk = ImageTk.PhotoImage(image=img)



cv2.imshow("Imagn",res)
cv2.waitKey(0)
cv2.destroyAllWindows()

