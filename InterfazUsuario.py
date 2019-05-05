import wx
from wx.lib import statbmp
import cv2
import numpy as np
import os
import traceback
import math
import threading,time

from LeerCelda import CeldaSincronizacion
from coloresReferencia import coloresReferencia
from SincronizacionCelda import Sincronizacion
from muestraDeColor import muestraDeColor
from Trama import Trama
global tramaGuardada
tramaGuardada = 0

class ComboBoxGeneral:
    def __init__(self, id, texto):
        """Constructor"""
        self.id = id
        self.texto = texto


class Camara:
    def __init__(self):
        self.resolucionx = 0
        self.resoluciony = 0
        self.velocidadCaptura = 0
        size=300, 300, 3
        self.captura=np.zeros(size, dtype=np.uint8)

    def onButton(event):
        print("")

    def iniciarCaptura(event):
        captura = cv2.VideoCapture(1)
        captura.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'XVID'))
        captura.set(cv2.CAP_PROP_AUTOFOCUS, 0)


class ShowCapture(wx.Frame):
    def __init__(self, capture, title, fps=30):
        wx.Frame.__init__(self, None,-1, title, size = (1350,745), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        panel = wx.Panel(self, -1)
        self.SetBackgroundColour((255, 255, 255))
        self.tamanoMatriz = 14
        self.sincronizacionAnterior=[[255,255,255],[255,255,255],[255,255,255]]
        
        self.capture = capture
        self.numColores = 2
        ret, frame = self.capture.read()
        
        height, width = frame.shape[:2]
        self.orig_height = height
        self.orig_width = width

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        
        self.tramasRecibidas = np.array([],dtype=int)
        self.cargaUtil = []
        self.datos = np.array([],dtype=int)
        self.frames = []
        self.cont = 0
        #create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(1000./self.fps)

        segundos = 40
        hilo = threading.Thread(target=self.NextFrame, 
                            args=(segundos,))
        

        #self.Bind(wx.EVT_TIMER, hilo.start())        
        hilo.start()

        patrones_segundo = [ComboBoxGeneral(15, "15"),
                ComboBoxGeneral(30, "30")]

        dimensiones = [ComboBoxGeneral(8, "8"),
                ComboBoxGeneral(10, "10"),ComboBoxGeneral(12, "12"),ComboBoxGeneral(14, "14"),ComboBoxGeneral(16, "16")]
        colores = [ComboBoxGeneral(2, "2"),
                ComboBoxGeneral(4, "4"),
                ComboBoxGeneral(8, "8")]

        sampleList = []

        font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Textos de combobox

        lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt1 = "Número de patrones por segundo"

        lb2 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt2 = "Tamaño"

        lb3 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt3 = "Número de colores"

        button = wx.Button(panel, wx.ID_ANY, 'Comenzar captura', (20, 400))
        #bind timer events to the handler
        
        button.Bind(wx.EVT_BUTTON, Camara.onButton)

        
        button1 = wx.Button(panel, wx.ID_ANY, 'Parar captura', (150, 400))
        button1.Bind(wx.EVT_BUTTON, Camara.onButton)


        lbl.SetFont(font)
        lbl.SetLabel(txt1)

        lb2.SetFont(font)
        lb2.SetLabel(txt2)

        lb3.SetFont(font)
        lb3.SetLabel(txt3)

        self.cb = wx.ComboBox(panel,-1,size=(150,100),choices=sampleList)
        self.cb1 = wx.ComboBox(panel,-1,size=(150,100),choices=sampleList)
        self.cb2 = wx.ComboBox(panel,-1,size=(150,100),choices=sampleList)

        self.widgetMaker(self.cb, patrones_segundo,self.onSelectFrecuencia)
        self.widgetMaker(self.cb1, dimensiones,self.onSelectTamano)
        self.widgetMaker(self.cb2, colores,self.onSelectColores)


        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        #add image widgets to the sizer grid
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lbl,0,wx.ALIGN_LEFT|wx.LEFT,25)
        sizer.Add(self.cb, 0,wx.LEFT|wx.ALIGN_LEFT, 20)

        sizer.Add(lb2,0,wx.ALIGN_LEFT|wx.LEFT,25)
        sizer.Add(self.cb1, 0,wx.LEFT|wx.ALIGN_LEFT,20)

        sizer.Add(lb3,0,wx.ALIGN_LEFT|wx.LEFT,25)
        sizer.Add(self.cb2, 0,wx.LEFT|wx.ALIGN_LEFT, 20)


        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.ImgControl,0,wx.LEFT|wx.ALIGN_RIGHT,100)

        sizer3 = wx.BoxSizer(wx.VERTICAL)

        lb4 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt4 = "FER"

        lb5 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt5 = "BER"

        lb4.SetFont(font)
        lb4.SetLabel(txt4)

        lb5.SetFont(font)
        lb5.SetLabel(txt5)

        sizer3.Add(lb4,0,wx.ALIGN_LEFT|wx.LEFT,25)
        sizer3.Add(lb5,0,wx.ALIGN_LEFT|wx.LEFT,25)

        sizer2.Add(sizer, 0, wx.EXPAND)
        sizer2.Add(sizer1, 0, wx.EXPAND)
        sizer2.Add(sizer3, 0, wx.EXPAND)
        panel.SetSizer(sizer2)

    #----------------------------------------------------------------------
    def widgetMaker(self, widget, objects,accion):
        for obj in objects:
            widget.Append(obj.texto, obj)
        widget.Bind(wx.EVT_COMBOBOX,accion)

    #----------------------------------------------------------------------
    def onSelectFrecuencia(self, event):
        print( "You selected: frecuencia " + self.cb.GetStringSelection())
        obj = self.cb.GetClientData(self.cb.GetSelection())
        self.fps = obj.id

    def onSelectTamano(self, event):
        print( "You selected: Tamaño " + self.cb1.GetStringSelection())
        obj = self.cb1.GetClientData(self.cb1.GetSelection())
        self.tamanoMatriz = obj.id

    def onSelectColores(self, event):
        print( "You selected: colores " + self.cb2.GetStringSelection())
        obj = self.cb2.GetClientData(self.cb2.GetSelection())
        self.numColores = obj.id

    def frombits(self,bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

    def leerTramas(self,dst2):
        imagen = coloresReferencia(dst2,self.tamanoMatriz,self.numColores)
        coloresR = imagen.obtenerColoresReferencia()
        matriz = muestraDeColor(dst2,self.tamanoMatriz,coloresR,self.numColores)
        bits = matriz.mapeoaBit()
        trama = Trama(bits,self.tamanoMatriz,self.numColores)
        
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
        img = cv2.imread('Nuevo16-0.png')
        c=1
        while img is not None:
            self.leerTramas(img)
            img = cv2.imread('Nuevo16-'+str(c)+'.png')
            c = c+1

    def NextFrame(self,segundos):
        
        contador = 0
        inicial = time.time()
        limite = inicial + segundos

        while inicial<=limite:
            #print(inicial, limite)
            inicial = time.time()
            ret, self.orig_frame = self.capture.read()

            if ret:
                frame = self.orig_frame
                bilFilter = cv2.bilateralFilter(frame,9,75,75)
                gray = cv2.cvtColor(bilFilter, cv2.COLOR_BGR2GRAY)
                cv2.imshow('gry',gray)

                ret,thresh = cv2.threshold(gray,200,255,1)
                contours,h = cv2.findContours(thresh,1,2)
                cv2.imshow('vhf',thresh)
                
                #cv2.imwrite("Nuevo16-"+str(inicial)+".png", frame)
                for i,cnt in enumerate(contours):
                    
                    approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
                    area = cv2.contourArea(cnt)
                    tamanoFinal = (self.tamanoMatriz + 4)*20
                    #print(area)
                    if len(approx)==4 and area > 9000 and area<270000:
                        
                        #cv2.drawContours(frame,cnt,-1,(255,0,255),3)
                        #cv2.imshow('',thresh)
                        #print(area)
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

                        M = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
                        dst2 = cv2.warpAffine(dst2,M,(cols,rows))
                        

                        nlineas = self.tamanoMatriz+3
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

                        coloresR = coloresReferencia(dst2,self.tamanoMatriz,self.numColores)
                        #print(coloresR.obtenerColoresReferencia())
                        sincronizacion=CeldaSincronizacion(self.tamanoMatriz)
                        celdaSincronizacion=sincronizacion.LeerCeldas(dst2)
                        FuncionSincronizacion=Sincronizacion(celdaSincronizacion,self.sincronizacionAnterior)
                        comparar=FuncionSincronizacion.CompararCeldas()
                        self.sincronizacionAnterior = celdaSincronizacion
                        
                        if comparar==1:
                            print('sincronización igual')
                            if self.cont == 1:
                                 hilo2 = threading.Thread(target=self.leerFrames)
                                 hilo2.start()
                            cv2.imwrite("Nuevo16-"+str(self.cont)+".png", dst2)
                            
                            self.cont = self.cont+1

                        else: 
                            print('sincronización nuevo')
                            if self.cont == 1:
                                 hilo2 = threading.Thread(target=self.leerFrames)
                                 hilo2.start()
                            cv2.imwrite("Nuevo16-"+str(self.cont)+".png", dst2)
                            self.cont = self.cont+1
                            #cv2.imwrite("ANterior16-"+str(i-1)+".png", dst)

                #self.bmp.CopyFromBuffer(dst)
                #self.ImgControl.SetBitmap(self.bmp)

captura = cv2.VideoCapture(1)
#captura = cv2.VideoCapture('http://192.168.1.72:4747/video')
captura.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
captura.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
captura.set(cv2.CAP_PROP_FPS, 60)

app = wx.App()
frame = ShowCapture(captura,'Receptor')
frame.Show()
app.MainLoop()
print(self.frames.shape())
