"""
Thiago S.  12/02/21
Adaptado do código do Daniel C.: <https://github.com/camposdp/emg-monitor>
Objetivo: receber os dados coletados com o esp32 (freq. de 1000 Hz) 
Pacote com buffer (200 linhas e 4 colunas). Cada coluna representa um sensor 
"""

from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from random import randint
import socket
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime

######################################
#Initial parameters

#HOST = socket.gethostbyname(socket.gethostname())
HOST = '192.168.4.1'  # Manual host enter
PORT = 80  # Port 

vountario = 'Thiago S. - CPGEI'
Nome_Arquivo = "C:\\Users\\tsimo\\Desktop\\Codigo_Esp32_Dt\\coletaww.txt"

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################
pg.setConfigOption('background', 'w') #to config the background color 
win = pg.GraphicsWindow(title="EMG Signals") # creates a window  pen='b'

p1 = win.addPlot(title="Signals from EMG system")  # creates empty space for the plot in the window
#p1.showGrid(x=True,y=True)
p1.addLegend()
p1.setYRange(0,2000)
curve1 = p1.plot(pen='b', name='Canal 1')                        # create an empty "plot" (a curve to plot)
curve2 = p1.plot(pen='r', name='Canal 2') 
curve3 = p1.plot(pen='g', name='Canal 3')                        # create an empty "plot" (a curve to plot)
curve4 = p1.plot(pen='y', name='Canal 4') 

windowWidth = 200                       # width of the window displaying the curve
Xm1 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr1 = -windowWidth                      # set first x position

Xm2 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr2 = -windowWidth                      # set first x position

Xm3 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr3 = -windowWidth                      # set first x position

Xm4 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr4 = -windowWidth                      # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update(data1, data2, data3, data4):
    global curve1, curve2, curve3, curve4, ptr1, ptr2, ptr3, ptr4, Xm1, Xm2, Xm3, Xm4   
    Xm1[:-1] = Xm1[1:]
    Xm2[:-1] = Xm2[1:]                      # shift data in the temporal mean 1 sample left
    Xm3[:-1] = Xm3[1:]
    Xm4[:-1] = Xm4[1:] 
    value1 = data1
    value2 = data2               # read line (single value) from the serial port
    value3 = data3
    value4 = data4               # read line (single value) from the serial port
    Xm1[-1] = float(value1)                 # vector containing the instantaneous values      
    Xm2[-1] = float(value2)
    Xm3[-1] = float(value3)                 # vector containing the instantaneous values      
    Xm4[-1] = float(value4)
    ptr1 += 1  
    ptr2 += 1                              # update x position for displaying the curve
    ptr3 += 1  
    ptr4 += 1                              # update x position for displaying the curve
    curve1.setData(Xm1)                     # set the curve with this data
    curve1.setPos(ptr1,0)                   # set x position in the graph to 0
    curve2.setData(Xm2)                     # set the curve with this data
    curve2.setPos(ptr2,0)                   # set x position in the graph to 0
    curve3.setData(Xm3)                     # set the curve with this data
    curve3.setPos(ptr3,0)                   # set x position in the graph to 0
    curve4.setData(Xm4)                     # set the curve with this data
    curve4.setPos(ptr4,0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now

#Main function
def connected(c):
    
    global msg

    while True:      

        msg = c.recv(16384) #receive data...

        if msg is not None:
            t = tempo = time.time()
            #now = datetime.now() #print(type(msg)) #bytes
            a = json.loads(msg) #print(type(a)) #dict
            df = pd.DataFrame(a)  #transforma o dicionário em DataFrame - print(df.head())
            #print(df.tail())
            #print("Antes:", time.time())
            update(str(t), df['data2'][5], df['data3'][5], df['data4'][5]) #Plota data from EMG System
            #print("Depois:", time.time())
            arquivo = open(Nome_Arquivo, "a", newline="")
            #arquivo.write(str(t)+str('-')+str(now.hour)+str(':')+str(now.minute)+str(':')+str(now.second)+str(':')+str(now.microsecond)+str(df.values))
            arquivo.write(str(t)+str(df.values))
            arquivo.write('\n')
            arquivo.close()
            
                      
######################################
# Main Code
######################################
                
#Create Socket                
sock = socket.socket()
sock.connect((HOST, PORT)) #Conecta-se ao servidor (Esp32)
#tcp.bind(orig)
#tcp.listen(1)


while True:
    try:
        connected(sock)
        
    except Exception as e: pass #print(e) 
    

sock.close()
### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
