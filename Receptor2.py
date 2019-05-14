from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from time import sleep
from videocaptureasync import VideoCaptureAsync
from PIL import Image, ImageTk
from os import remove
import threading,time

import cv2
import tkinter as tkk
import sys
import numpy as np
import math

from LeerCelda import CeldaSincronizacion
from coloresReferencia import coloresReferencia
from SincronizacionCelda import Sincronizacion
from muestraDeColor import muestraDeColor
from Trama import Trama
from rotarImagen import rotarImagen
global tramaGuardada
tramaGuardada = 0


class Interfaz:
    def __init__(self):
        self.Interfaz = Tk()
        self.Interfaz.state('zoomed')
        self.Interfaz.configure(bg='#636363')
        self.cap = None
        self.hilo2 = None
        self.sincronizacionAnterior=[[255,255,255],[255,255,255],[255,255,255]]
        self.tramasRecibidas = np.array([],dtype=int)
        self.cargaUtil = []
        self.datos = np.array([],dtype=int)
        self.frames = []
        self.cont = 0

        #PATRONES POR SEGUNDO
        self.etiqueta = Label(text="FPS: ").place(relx=0.05,rely=0.15)
        self.patronesPorSegundo = ttk.Combobox(state="readonly", values=[30,60])
        self.patronesPorSegundo.place(relx=0.15,rely=0.15)
        self.patronesPorSegundo.current(0)

        #TAMAÑO DE LA MATRIZ
        self.etiqueta2 = Label(text="Tamaño de la matriz: ").place(relx=0.05,rely=0.2)
        self.tamanoMatriz = ttk.Combobox(state="readonly", values=[8,10,12,14,16,100])
        self.tamanoMatriz.place(relx=0.15,rely=0.2)
        self.tamanoMatriz.current(0)
        
        #NUMERO DE COLORES
        self.etiqueta3 = Label(text="Número de colores").place(relx=0.05,rely=0.25)
        self.numeroColores = ttk.Combobox(state="readonly", values=[2,4,8])
        self.numeroColores.place(relx=0.15,rely=0.25)
        self.numeroColores.current(0)
        
        segundos = 45
        self.borrarImagenes()
        self.hilo = threading.Thread(target=self.IniciarCaptura, 
                            args=(segundos,))

        self.transmitir = Button(self.Interfaz,text="Comenzar Captura",command=self.hilo.start).place(relx=0.05,rely=0.35)
        self.transmitir = Button(self.Interfaz,text="Parar Captura",command=self.PararCaptura).place(relx=0.15,rely=0.35)
        #self.scrolledtext1 = st.ScrolledText(self.Interfaz, width=30, height=20)
        #self.scrolledtext1.place(relx=0.1, rely=0.35)
        

        #PRUEBA DE IMAGEN EN LABEL
        self.l1 = tkk.Label(self.Interfaz, text="   ", borderwidth=4, relief="groove")
        self.l1.place(relx=0.30,rely=0.005,width=300, height=300)
        
        #TRAMAS
        self.etiquetaR = Label(text="Tramas recibidas - de: ").place(relx=0.6,rely=0.15)

        #FER
        self.etiquetaF = Label(text="FER: ").place(relx=0.6,rely=0.25)
        #BER
        self.etiquetaB = Label(text="BER: ").place(relx=0.6,rely=0.35)

        self.Interfaz.mainloop()

    def borrarImagenes(self):
        c=0
        img = cv2.imread('Nuevo16-0.png')
        while img is not None:
            remove('Nuevo16-'+str(c)+'.png')
            c = c+1
            img = cv2.imread('Nuevo16-'+str(c)+'.png')
        
    def frombits(self,bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

    def leerTramas(self,dst2):
        imagen = coloresReferencia(dst2,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
        coloresR = imagen.obtenerColoresReferencia()
        matriz = muestraDeColor(dst2,int(self.tamanoMatriz.get()),coloresR,int(self.numeroColores.get()))
        bits = matriz.mapeoaBit()
        trama = Trama(bits,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
        
        trama.obtenerCampos()

        if trama.tramaValida == True:
            if not self.cargaUtil:
                self.cargaUtil = np.ones((trama.numeroTramas,1),dtype=int)
                self.cargaUtil = self.cargaUtil.tolist()

            print("Trama: ",trama.numeroDeTrama," de ", trama.numeroTramas," tramas")
            print("valida")

            if trama.numeroDeTrama in self.tramasRecibidas:
                print("La trama ya esta")
            else:
                self.tramasRecibidas = np.concatenate((self.tramasRecibidas,trama.numeroDeTrama),axis=None)
                print("Tramas recibidas: ",self.tramasRecibidas)
                self.cargaUtil[trama.numeroDeTrama-1] = trama.cargaUtil

                if self.tramasRecibidas.shape[0] == trama.numeroTramas:
                    for h in range(trama.numeroTramas):
                        self.datos = np.concatenate((self.datos,self.cargaUtil[h]),axis=None)

                    print("Se recibieron todas las tramas")
                    print(self.datos)
                    print(self.frombits(self.datos))
        else:
            print("invalida")
        
    def leerFrames(self):
        #img = cv2.imread('Nuevo16-0.png')
        #c=1
        #while img is not None:
        img = cv2.imread('Nuevo16-'+str( threading.current_thread().getName())+'.png')
        self.leerTramas(img)
        print("Nuevo16-"+str( threading.current_thread().getName()))
        print("******************************************")
        #c = c+1

    def IniciarCaptura(self,segundos):
        
        if self.patronesPorSegundo.get() == 30:
            self.cap = VideoCaptureAsync(0,1920,1080,30)
        else:
            self.cap = VideoCaptureAsync(0,1280,720,60)
        self.cap.start()

        contador = 0
        inicial = time.time()
        limite = inicial + segundos

        while self.cap.isOpened():
            while inicial<=limite:
                inicial = time.time()
            
                try:
                    ret, frame = self.cap.read()
                    if ret:

                        bilFilter = cv2.bilateralFilter(frame,9,75,75)
                        gray = cv2.cvtColor(bilFilter, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('gry',gray)
                        cv2.imwrite("NuevoGris.png", gray)

                        ret,thresh = cv2.threshold(gray,200,255,1)
                        _,contours,h = cv2.findContours(thresh,1,2)
                        cv2.imshow('vhf',thresh)
                        cv2.imwrite("NuevoNegro.png", thresh)

                        for i,cnt in enumerate(contours):
                    
                            approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
                            area = cv2.contourArea(cnt)
                            auxT=int(self.tamanoMatriz.get())+4
                            tamanoFinal = auxT*20

                            if len(approx)==4 and area > 9000 and area<270000:

                                approx1=[approx[0],approx[1],approx[3],approx[2]]
                                pts1 = np.float32(approx1)
                                pts2 = np.float32([[0,0],[0,tamanoFinal],[tamanoFinal,0],[tamanoFinal,tamanoFinal]])
                                M = cv2.getPerspectiveTransform(pts1,pts2)
                                dst = cv2.warpPerspective(frame,M,(tamanoFinal,tamanoFinal))
                        
                                img = dst
                                gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                                ret,thresh2 = cv2.threshold(gray2,155,255,1)
                                cv2.imshow("GRIS",thresh2)
                                cv2.imshow("gris2",gray2)

                                imgScreen = Image.fromarray(dst)
                                imgtk = ImageTk.PhotoImage(image=imgScreen)
                                self.l1.imgtk = imgtk
                                self.l1.configure(image = imgtk)
                                self.Interfaz.update()
                                
                                # Remove some small noise if any.
                                dilate = cv2.dilate(thresh2,None)
                                erode = cv2.erode(dilate,None)

                                # Find contours with cv2.RETR_CCOMP
                                _,contours,hierarchy = cv2.findContours(erode,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                                #cv2.drawContours(img,contours,-1,(255,0,255),3)
                        
                                e1x = 300
                                e2x = 0
                                e1y = 300
                                e2y = 0

                                for p,cnt in enumerate(contours):
                                # Check if it is an external contour and its area is more than 100

                                    if hierarchy[0,p,3] == -1 and cv2.contourArea(cnt)>300:
                                        x,y,w,h = cv2.boundingRect(cnt)
                                        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                                
                                        #cv2.circle(img,(x,y), 2, (0,0,255), -1)
                                        #print(format(x)+'--'+format(y))
                                        #cv2.imshow('Segundo',img)
                                        if x<=e1x+8 and y<=e1y:
                                            e1x = x
                                            e1y = y
                                            #print(format(x)+'-2-'+format(y))
                                    
                                        if x+w>e2x and y+h>e2y:
                                            e2x = x+w
                                            e2y = y+h
                                            cv2.circle(img,(x+w,y+h), 2, (0,255,0), -1)

                                #cv2.rectangle(img,(e1x,e1y),(e2x,e2y),(0,255,0),2)
                                #cv2.imshow('Segundo',img)

                                pts1 = np.float32([[e1x,e1y],[e2x,e1y],[e1x,e2y],[e2x,e2y]])
                                pts2 = np.float32([[0,0],[0,tamanoFinal],[tamanoFinal,0],[tamanoFinal,tamanoFinal]])
                                M = cv2.getPerspectiveTransform(pts1,pts2)
                                dst2 = cv2.warpPerspective(img,M,(tamanoFinal,tamanoFinal))

                                rows,cols = dst2.shape[:2]

                                r = rotarImagen(dst2,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
                                dst2 = r.rotar()

                                nlineas = int(self.tamanoMatriz.get())+3
                                tcuadrado = round(tamanoFinal/(nlineas+1))
                                for x in range(nlineas):
                                #lineas verticales
                                    pt1 = ((x+1)*tcuadrado,0)
                                    pt2 = ((x+1)*tcuadrado,tamanoFinal)
                                    cv2.line(dst2,pt1,pt2,(0,255,0),1)

                                    #lineas horizontales
                                    pt1 = (0,(x+1)*tcuadrado)
                                    pt2 = (tamanoFinal,(x+1)*tcuadrado)
                                    cv2.line(dst2,pt1,pt2,(0,255,0),1)
                                cv2.imshow("Transformacion2", dst2)

                                coloresR = coloresReferencia(dst2,self.tamanoMatriz.get(),self.numeroColores.get())
                                #print(coloresR.obtenerColoresReferencia())
                                sincronizacion=CeldaSincronizacion(self.tamanoMatriz.get())
                                celdaSincronizacion=sincronizacion.LeerCeldas(dst2)
                                FuncionSincronizacion=Sincronizacion(celdaSincronizacion,self.sincronizacionAnterior)
                                comparar=FuncionSincronizacion.CompararCeldas()
                                self.sincronizacionAnterior = celdaSincronizacion
                        
                                #if comparar==1:
                                print('sincronización igual')
                                #if self.cont == 1:
                                #    hilo2 = threading.Thread(target=self.leerFrames)
                                #    hilo2.start()
                                cv2.imwrite("Nuevo16-"+str(self.cont)+".png", dst2)
                                print("Nuevo16-"+str(self.cont))
                                   
                                hilo2 = threading.Thread(name='%s' %self.cont, 
                                                        target=self.leerFrames)    
                                hilo2.start()
                                self.cont = self.cont+1

                                #else: 
                                #    print('sincronización nuevo')
                                #    if self.cont == 1:
                                #        hilo2 = threading.Thread(target=self.leerFrames)
                                #        hilo2.start()
                                #    cv2.imwrite("Nuevo16-"+str(self.cont)+".png", dst2)
                                #    print("Nuevo16-"+str(self.cont))
                                #    self.cont = self.cont+1

                except KeyboardInterrupt:
                    #pass
                    exit()

    
    def PararCaptura(self):
        #self.hilo.join()
        #cv2.destroyAllWindows()
        self.cap.stop()
        self.cap.exit()
        
            
aplicacion1=Interfaz()
exit()

