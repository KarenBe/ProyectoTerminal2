from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from time import sleep
from time import time
from threading import Lock
from videocaptureasync import VideoCaptureAsync
from PIL import Image, ImageTk
from os import remove
import threading,time
import subprocess
import os
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
        self.numTramas = 0
        self.tramasValidas = 0
        self.tramasInvalidas = 0
        self.tiempoInicial = 0
        self.tiempoFinal = 0
        self.tiempoTotal = 0
        self.TramasFaltantes = 0

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

        #SEGUNDOS
        self.etiqueta3 = Label(text="Segundos capturados").place(relx=0.05,rely=0.3)
        self.segundos = ttk.Combobox(state="readonly", values=[1,2,3,4,5,6,7,8,9,10])
        self.segundos.place(relx=0.15,rely=0.3)
        self.segundos.current(0)

        self.borrarImagenes()

        #self.hilo = threading.Thread(target=self.IniciarCaptura2, 
        #                    args=(5,))

        self.transmitir = Button(self.Interfaz,text="Comenzar Captura",command=self.IniciarProcesamiento).place(relx=0.05,rely=0.35)
        self.transmitir = Button(self.Interfaz,text="Parar Captura",command=self.PararCaptura).place(relx=0.15,rely=0.35)
        #self.scrolledtext1 = st.ScrolledText(self.Interfaz, width=30, height=20)
        #self.scrolledtext1.place(relx=0.1, rely=0.35)
        

        #PRUEBA DE IMAGEN EN LABEL
        self.l1 = tkk.Label(self.Interfaz, text="   ", borderwidth=4, relief="groove")
        self.l1.place(relx=0.30,rely=0.1,width=300, height=300)
        
        #TRAMAS
        self.TR = StringVar()
        self.TF = StringVar()
        self.etiquetaR = Label(self.Interfaz,textvariable=self.TR).place(relx=0.6,rely=0.15)
        self.etiquetaFa = Label(self.Interfaz,textvariable=self.TF).place(relx=0.6,rely=0.20)

        self.TR.set("Tramas Recibidas: ")
        self.TF.set("Tramas Faltantes: ")

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

        for file in os.listdir("."):
            if os.path.isfile(file) and file.startswith("Nuevo_"):
                os.remove(file)

        
    def frombits(self,bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

    def leerTramas(self,dst2):
        if self.numTramas == 0:
            imagen = coloresReferencia(dst2,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
            coloresR = imagen.obtenerColoresReferencia()
            matriz = muestraDeColor(dst2,int(self.tamanoMatriz.get()),coloresR,int(self.numeroColores.get()))
            bits = matriz.mapeoaBit()
            trama = Trama(bits,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
            trama.obtenerCampos()

            if trama.tramaValida == True:
                self.numTramas = trama.numeroTramas
                if not self.cargaUtil:
                    self.cargaUtil = np.ones((trama.numeroTramas,1),dtype=int)
                    self.cargaUtil = self.cargaUtil.tolist()

                self.tramasRecibidas = np.concatenate((self.tramasRecibidas,trama.numeroDeTrama),axis=None)
                print("Tramas recibidas: ",self.tramasRecibidas)
                self.cargaUtil[trama.numeroDeTrama-1] = trama.cargaUtil
                self.tramasValidas += 1
                print("valida")
            else:
                self.tramasInvalidas += 1
                print("trama invalida")
        else:
            imagen = coloresReferencia(dst2,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
            coloresR = imagen.obtenerColoresReferencia()
            matriz = muestraDeColor(dst2,int(self.tamanoMatriz.get()),coloresR,int(self.numeroColores.get()))
            bits = matriz.indicadores()
            trama = Trama(bits,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
            trama.obtenerIndicadores()

            if trama.numeroTramas == self.numTramas and trama.numeroDeTrama<=self.numTramas and trama.numeroDeTrama>0:
                if trama.numeroDeTrama in self.tramasRecibidas:
                    print("La trama ya esta")
                    bits = matriz.mapeoaBit()
                    trama = Trama(bits,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
                    trama.obtenerCampos()

                    if trama.tramaValida == True:
                        print("trama valida")
                        self.tramasValidas += 1
                    else:
                        print("trama invalida")
                        self.tramasInvalidas += 1

                else:
                    bits = matriz.mapeoaBit()
                    trama = Trama(bits,int(self.tamanoMatriz.get()),int(self.numeroColores.get()))
                    trama.obtenerCampos()
                    
                    if trama.tramaValida == True:
                        self.tramasRecibidas = np.concatenate((self.tramasRecibidas,trama.numeroDeTrama),axis=None)
                        print("Tramas recibidas: ",self.tramasRecibidas)
                        self.TramasFaltantes=self.numTramas - self.tramasRecibidas.shape[0]
                        print("Tramas faltantes: ",self.TramasFaltantes)
                        self.cargaUtil[trama.numeroDeTrama-1] = trama.cargaUtil
                        self.tramasValidas +=1

                        self.TR.set("Tramas Recibidas: "+format(self.tramasRecibidas))
                        self.TF.set("Tramas Faltantes: "+format(self.TramasFaltantes))
                        self.Interfaz.update()
                        if self.tramasRecibidas.shape[0] == trama.numeroTramas:
                            for h in range(trama.numeroTramas):
                                self.datos = np.concatenate((self.datos,self.cargaUtil[h]),axis=None)
                            print("Se recibieron todas las tramas")
                            self.tiempoFinal = time.time()
                            self.tiempoTotal = self.tiempoFinal - self.tiempoInicial
                            print("Tramas validas: ", self.tramasValidas)
                            print("Tramas invalidas: ",self.tramasInvalidas)
                            print("Bits recibidos: ",self.datos.shape[0])
                            print("Tiempo: ",self.tiempoTotal)
                            mb.showinfo(message="Se recibieron todas las tramas", title="Título")
                            file = open('texto.txt','a')
                            file.write(self.frombits(self.datos))
                            file.close()
                            subprocess.run(["notepad","texto.txt"])
                    else:
                        self.tramasInvalidas += 1
                        print("invalida")
        
    def leerFrames(self):
        frame = cv2.imread('Nuevo16-0.png')
        c=0
        
        while frame is not None:
            bilFilter = cv2.bilateralFilter(frame,9,75,75)
            gray = cv2.cvtColor(bilFilter, cv2.COLOR_BGR2GRAY)
            with Lock(): 
                cv2.imshow('gry',gray)
                cv2.waitKey(25)
            cv2.imwrite("NuevoGris.png", gray)

            ret,thresh = cv2.threshold(gray,200,255,1)
            contours,h = cv2.findContours(thresh,1,2)
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

                    # Remove some small noise if any.
                    dilate = cv2.dilate(thresh2,None)
                    erode = cv2.erode(dilate,None)

                    # Find contours with cv2.RETR_CCOMP
                    contours,hierarchy = cv2.findContours(erode,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
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
            
                    if comparar==1:
                        print('sincronización igual')
                    else:
                        print('sincronización nuevo')
                        self.leerTramas(dst2)
                        print("Nuevo16-"+str(c))
                        print("******************************************")
                        cv2.imwrite("Nuevo_16-"+str(c)+".png", dst2)
                        
                        nombreImagen = 'Nuevo_16-'+str(c)+'.png'
                        imgl = Image.open(nombreImagen)
                        imgl.thumbnail((300,300), Image.ANTIALIAS)
                        imgScreen = ImageTk.PhotoImage(imgl)
                        self.l1.configure(image = imgScreen)
                        self.Interfaz.update()
            #self.leerTramas(img)
            frame = cv2.imread('Nuevo16-'+str(c)+'.png')
            c = c+1
        print("Tramas validas: ",self.tramasValidas)
        print("Tramas invalidas: ",self.tramasInvalidas)
        print("Tramas totales: ", self.tramasInvalidas + self.tramasValidas)

    def IniciarProcesamiento(self):

        self.hilo = threading.Thread(target=self.IniciarCaptura2, 
                            args=(int(self.segundos.get()),))
        self.hilo.start()
    
    def IniciarCaptura2(self,segundos):  
        top = Toplevel()
        top.title("Información")
        msg = Message(top,width=300,text="                     Iniciando camara...                  ")
        msg.pack()

        self.tiempoInicial = time.time()
        if self.patronesPorSegundo.get() == 30:
            self.cap = VideoCaptureAsync(1,1920,1080,30)
        else:
            self.cap = VideoCaptureAsync(1,1280,720,60)
        self.cap.start()

        contador = 0
        inicial = time.time()
        limite = inicial + segundos
        
        while self.cap.isOpened():
            top.destroy()
            top = Toplevel()
            top.title("Información")
            msg = Message(top,width=300,text="                     Capturando...                  ")
            msg.pack()
            while inicial<=limite:
                inicial = time.time()
                try:
                    ret, frame = self.cap.read()
                    if ret:
                        cv2.imwrite("Nuevo16-"+str(contador)+".png", frame)
                        print("Nuevo16-",str(contador))
                        contador +=1           
                except KeyboardInterrupt:
                    #pass
                    exit()
            break
        top.destroy()
        hilo2 = threading.Thread(target=self.leerFrames)
        hilo2.start()          

    def IniciarCaptura(self,segundos):
        self.tiempoInicial = time.time()
        if self.patronesPorSegundo.get() == 30:
            self.cap = VideoCaptureAsync(1,1920,1080,30)
        else:
            self.cap = VideoCaptureAsync(1,1280,720,60)
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
                        with Lock(): 
                            cv2.imshow('gry',gray)
                            cv2.waitKey(25)
                        cv2.imwrite("NuevoGris.png", gray)

                        ret,thresh = cv2.threshold(gray,200,255,1)
                        contours,h = cv2.findContours(thresh,1,2)
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

                                
                                # Remove some small noise if any.
                                dilate = cv2.dilate(thresh2,None)
                                erode = cv2.erode(dilate,None)

                                # Find contours with cv2.RETR_CCOMP
                                contours,hierarchy = cv2.findContours(erode,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
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
                                #print('sincronización igual')
                                if self.cont == 1:
                                    hilo2 = threading.Thread(target=self.leerFrames)
                                    hilo2.start()
                                cv2.imwrite("Nuevo16-"+str(self.cont)+".png", dst2)
                                nombreImagen = 'Nuevo16-'+str(self.cont)+'.png'
                                imgScreen = PhotoImage(file = nombreImagen)
                                self.l1.configure(image = imgScreen)
                                self.Interfaz.update()
                                #print("Nuevo16-"+str(self.cont))
                                   
                                #hilo2 = threading.Thread(name='%s' %self.cont, 
                                #                        target=self.leerFrames)    
                                #hilo2.start()
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
        self.hilo.join()
        self.hilo.join()
        #cv2.destroyAllWindows()
        self.cap.stop()
        self.cap.exit()
        
            
aplicacion1=Interfaz()
exit()

