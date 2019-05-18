#!/usr/bin/env python

import cv2
import time
from threading import Lock

if __name__ == '__main__' :

    # Start default camera
    
    video = cv2.VideoCapture(1)
    #video.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}"+format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        altura = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        ancho = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print( "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}"+format(fps)+' altura: '+format(altura)+ 'ancho: '+format(ancho))

        #video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'XVID'))
        #video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
        #video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
        #fps = video.get(cv2.CAP_PROP_FPS)
        #print( "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}"+format(fps))
        print("x")

    # Number of frames to capture
    num_frames = 30;


    print( "Capturing {0} frames"+format(num_frames))

    # Start time
    start = time.time()
    tiempo=30
    tiempoF=start+tiempo
    # Grab a few frames
    print("Inicio")
    #for i in range(0, num_frames) :
    c=0
    while(start<tiempoF):
        ret, frame = video.read()
        bilFilter = cv2.bilateralFilter(frame,9,75,75)
        gray = cv2.cvtColor(bilFilter, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,1)
        contours,h = cv2.findContours(thresh,1,2)

        with Lock(): 
            cv2.imshow("NuevoNegro.png", thresh)
            cv2.waitKey(25)
        #cv2.imshow("NuevoGris.png", gray)

        
        #cv2.imshow('vhf',thresh)
        #cv2.imwrite("NuevoNegro.png", thresh)
        #cv2.imwrite("Nuevo16-"+str(c)+".png", frame)
        start=time.time()
        c+=1

    print("Frames: ",c)
    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds"+format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds;
    print ("Estimated frames per second : {0}"+format(fps));

    # Release video
    video.release()
