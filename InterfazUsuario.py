import wx
from wx.lib import statbmp
import cv2
import numpy as np
import os
import traceback



class ComboBoxGeneral:
    def __init__(self, id, texto):
        """Constructor"""
        self.id = id
        self.texto = texto

#hola
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

        self.tamanoMatriz = dimensiones
        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame[:2]
        self.bmp = wx.Bitmap.FromBuffer(300, 300, frame)
        
        #create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        self.Bind(wx.EVT_TIMER, self.NextFrame)

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

        self.widgetMaker(self.cb, patrones_segundo)
        self.widgetMaker(self.cb1, dimensiones)
        self.widgetMaker(self.cb2, colores)


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
    def widgetMaker(self, widget, objects):
        """"""
        for obj in objects:
            widget.Append(obj.texto, obj)
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)

    #----------------------------------------------------------------------
    def onSelect(self, event):
        """"""
        print( "You selected: " + self.cb.GetStringSelection())
        obj = self.cb.GetClientData(self.cb.GetSelection())
        text = """
        The object's attributes are:
        %s  %s

        """ % (obj.id, obj.texto)

        self.tamanoMatriz = obj.id
        print( text)
        cv2.destroyAllWindows()
        cam.velocidadCaptura=15


    def NextFrame(self,event):
            
        ret, self.orig_frame = self.capture.read()
        if ret:
            frame = self.orig_frame 

            bilFilter = cv2.bilateralFilter(frame,9,75,75)
            gray = cv2.cvtColor(bilFilter, cv2.COLOR_BGR2GRAY)

            ret,thresh = cv2.threshold(gray,150,255,1)
            contours,h = cv2.findContours(thresh,1,2)
            #cv2.drawContours(frame,contours,-1,(255,0,255),3)

            for i,cnt in enumerate(contours):
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                area = cv2.contourArea(cnt)
                if len(approx)==4 and area > 2000:

                    rect = cv2.boundingRect(cnt)
                    print(approx)
                    x,y,w,h = rect
                    #box = cv2.rectangle(frame, (x,y), (x+w,y+h),-1, 0)
                    cropped = frame[y-2: y+h+2, x-2: x+w+2]

                    approx1=[approx[0],approx[1],approx[3],approx[2]]

                    pts1 = np.float32(approx1)
                    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
                    M = cv2.getPerspectiveTransform(pts1,pts2)
                    dst = cv2.warpPerspective(frame,M,(300,300))

                    #DIBUJAR CUADRICULA
                    nlineas = self.tamanoMatriz+7
                    tcuadrado = int(700/(nlineas+1))
                    for x in range(nlineas):
                        #lineas verticales
                        pt1 = ((x+1)*tcuadrado,0)
                        pt2 = ((x+1)*tcuadrado,700)
                        cv2.line(img,pt1,pt2,(0,0,0),1)

                        #lineas horizontales
                        pt1 = (0,(x+1)*tcuadrado)
                        pt2 = (700,(x+1)*tcuadrado)
                        cv2.line(img,pt1,pt2,(0,0,0),1)
                    cv2.imshow("Transformacion", dst)
                    cv2.imwrite("img"+str(i)+".png", dst)

                    

            self.bmp.CopyFromBuffer(dst)
            self.ImgControl.SetBitmap(self.bmp)


captura = cv2.VideoCapture(1)


app = wx.App()
frame = ShowCapture(captura,'Receptor')
frame.Show()
app.MainLoop()
