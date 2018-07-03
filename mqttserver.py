

import sys
sys.path.append('../')
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import serial
import serial.tools.list_ports
import _winreg as winreg
import itertools
import serial, time, datetime, optparse, signal
from time import gmtime, strftime
from libs import list_ports_windows
import sys
import os
import json
import subprocess as sp
from simple_event import Event, EventDispatcher, ProgressEvent
import binascii
import threading, requests, time
import datetime
import win32api, win32con, win32gui
from ctypes import *
import os
import hashlib
import binascii
import os
import loralib
import vonxclib
windows = None 
from  vonxc import vonxc_pb2
import sys, os
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt4'
if not hasattr(sys, 'frozen'):
    if __file__ == '<stdin>':
        path = os.getcwd()
    else:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path.rstrip(os.path.sep)
    if 'pyqtgraph' in os.listdir(path):
        sys.path.insert(0, path) ## examples adjacent to pyqtgraph (as in source tree)
    else:
        for p in sys.path:
            if len(p) < 3:
                continue
            if path.startswith(p):  ## If the example is already in an importable location, promote that location
                sys.path.remove(p)
                sys.path.insert(0, p)

## should force example to use PySide instead of PyQt

from PyQt4 import QtGui
import pyqtgraph as pg    
    
## Force use of a specific graphics system
use_gs = 'default'
for gs in ['raster', 'native', 'opengl']:
    if gs in sys.argv:
        use_gs = gs
        QtGui.QApplication.setGraphicsSystem(gs)
        break

print("Using %s (%s graphics system)" % (pg.Qt.QT_LIB, use_gs))

## Enable fault handling to give more helpful error messages on crash. 
## Only available in python 3.3+
try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass
    
#import pyqtgraph as pg
#from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


import paho.mqtt.client as mqtt
import binascii






class BaseWindow(QtGui.QMainWindow):
    def __init__(self):
        super(BaseWindow, self).__init__()
    def load_ui(self,ui_file):
        uic.loadUi(ui_file, self)
        self.setWindowTitle('VonMQTTServer')
        self.pushButtonNetConnect.clicked.connect(self.on_pushButtonNetConnect)
        
        self.pushButtonSendlData.clicked.connect(self.on_pushButtonSendlData)
        self.pushButtonGetVersion.clicked.connect(self.on_pushButtonGetVersion)

        self.mw = self
        
        self.mw.treeWidgetRadioPacketLog.setColumnCount(4);
        header = QtGui.QTreeWidgetItem([" Timestamp "," TX/RX "," HEX ", "String "])
        self.mw.treeWidgetRadioPacketLog.setColumnWidth(0,200)
        self.mw.treeWidgetRadioPacketLog.setColumnWidth(1,50)
        self.mw.treeWidgetRadioPacketLog.setColumnWidth(2,400)
        self.mw.treeWidgetRadioPacketLog.setColumnWidth(3,400)
        self.mw.treeWidgetRadioPacketLog.setHeaderItem(header)
        
        self.mw.treeWidgetSensorIDList.setColumnCount(3);
        header = QtGui.QTreeWidgetItem([""," Name"," id    "])
        self.mw.treeWidgetSensorIDList.setColumnWidth(0,40)
        self.mw.treeWidgetSensorIDList.setColumnWidth(1,120)
        self.mw.treeWidgetSensorIDList.setColumnWidth(2,20)
        self.mw.treeWidgetSensorIDList.setHeaderItem(header)
        
        
        self.mw.treeWidgetMetritcIDList.setColumnCount(3);
        header = QtGui.QTreeWidgetItem([""," Name"," id    "])
        self.mw.treeWidgetMetritcIDList.setColumnWidth(0,40)
        self.mw.treeWidgetMetritcIDList.setColumnWidth(1,120)
        self.mw.treeWidgetMetritcIDList.setColumnWidth(2,20)
        self.mw.treeWidgetMetritcIDList.setHeaderItem(header)
        
        
        self.mw.treeWidgetDeviceConfigureIDList.setColumnCount(3);
        header = QtGui.QTreeWidgetItem([""," Name"," id    "])
        self.mw.treeWidgetDeviceConfigureIDList.setColumnWidth(0,40)
        self.mw.treeWidgetDeviceConfigureIDList.setColumnWidth(1,120)
        self.mw.treeWidgetDeviceConfigureIDList.setColumnWidth(2,20)
        self.mw.treeWidgetDeviceConfigureIDList.setHeaderItem(header)
     
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.pubTime = time.time()
     
        self.fwReceive = False
        
        self.mw.pushButtonRadioDeviceReset.clicked.connect(self.on_pushButtonRadioDeviceReset)
        self.mw.pushButtonRadioGetSerial.clicked.connect(self.on_pushButtonRadioGetSerial)
        self.mw.pushButtonRadioGetTime.clicked.connect(self.on_pushButtonRadioGetTime)
        self.mw.pushButtonRadioFWupdate.clicked.connect(self.on_pushButtonRadioFWupdate)
        
        
        self.mw.pushButtonRadioFileUpload.clicked.connect(self.on_pushButtonRadioFileUpload)
        self.mw.pushButtonBuildConfigFileRead.clicked.connect(self.on_pushButtonBuildConfigFileRead)
        
        self.mw.pushButtonRadioFileDelete.clicked.connect(self.on_pushButtonRadioFileDelete)
        self.mw.pushButtonGetRadioSensorValue.clicked.connect(self.on_pushButtonGetRadioSensorValue)
        self.mw.pushButtonGetRadioMetricValue.clicked.connect(self.on_pushButtonGetRadioMetricValue)
        self.mw.pushButtonGetRadioConfigureValue.clicked.connect(self.on_pushButtonGetRadioConfigureValue)
        self.mw.pushButtonRadioConsole.clicked.connect(self.on_pushButtonRadioConsole)
        
        
      
        
        self.loralib = loralib.LoraParser()
        self.isLORA = False
        self.vonxcRadioLib = vonxclib.ProtobufFormatter()
        #self.vonxcRadioLib.serialize({"device_control":"VERSION_ID","VERSION_ID":""})
        if self.isLORA:
            for x in self.loralib.getValueList():
                self.mw.comboBoxDeviceControl.addItem(str(x['name']))
        else:
            self.mw.treeWidgetSensorIDList.clear()
            nCount = 0 
            l = [] 
            for x in self.vonxcRadioLib.getSensorList():
                #print x
                aRow = ["",str(x['name']),str(x['id'])]
                #print aRow
            
                item = QtGui.QTreeWidgetItem(aRow) 
                item.setCheckState(0, Qt.Unchecked)
                l.append (item)
            self.mw.treeWidgetSensorIDList.addTopLevelItems(l)   
    
        
        
        if self.isLORA:
            for x in self.loralib.getValueList():
                self.mw.comboBoxDeviceControl.addItem(str(x['name']))
        else:
            self.mw.treeWidgetMetritcIDList.clear()
            nCount = 0 
            l = [] 
            for x in self.vonxcRadioLib.getMetricList():
                print x
                aRow = ["",str(x['name']),str(x['id'])]
                print aRow
            
                item = QtGui.QTreeWidgetItem(aRow) 
                item.setCheckState(0, Qt.Unchecked)
                l.append (item)
            self.mw.treeWidgetMetritcIDList.addTopLevelItems(l)

        if self.isLORA:
            for x in self.loralib.getValueList():
                self.mw.comboBoxDeviceControl.addItem(str(x['name']))
        else:
            self.mw.treeWidgetDeviceConfigureIDList.clear()
            nCount = 0 
            l = [] 
            for x in self.vonxcRadioLib.getDeviceConfigureList():
                print x
                aRow = ["",str(x['name']),str(x['id'])]
                print aRow
            
                item = QtGui.QTreeWidgetItem(aRow) 
                item.setCheckState(0, Qt.Unchecked)
                l.append (item)
            self.mw.treeWidgetDeviceConfigureIDList.addTopLevelItems(l)

    def on_pushButtonRadioConsole(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'CLI_CHANGE'
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            pass
            
    def on_pushButtonBuildConfigFileRead(self):
    
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:

            self.path = str(self.mw.lineEditRadioTXInfo.text()) 
            print "textfile" , str(self.mw.lineEditRadioTXInfo.text()) 
            base=os.path.basename(self.path)
            dict = {}
            dict['device_control'] = 'FILE_OPEN_ID'
            dict['value'] = "/frt/"+base
            dict['mode'] = 0x00 #FILE_READ
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            dict['device_control'] = 'FILE_CLOSE_ID'
            dict['id'] = 1
            
            progress = 0
            self.valuString = ''
            while True :
                returnValue  = self.build_file_read(1,64, progress,1000)
                if  returnValue == None:
                    break 
                print ">>>>>>>>>>>>>>>>>>>>>>>>" ,binascii.hexlify(returnValue)
                self.valuString = returnValue + self.valuString 
                if  len(returnValue) != 64:
                    break 
                progress  = progress +  len(returnValue)    
      
            dict['device_control'] = 'FILE_CLOSE_ID'
            dict['id'] = 1
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            
            with open(base, "wb") as bin_file:                      
                        bin_file.write(self.valuString)
                        bin_file.close()
                        osCommandString = "notepad.exe "+base
                        os.system(osCommandString)
                       

            
 
        pass
        
       
        
    def on_pushButtonRadioFileDelete(self): 
    
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_DELETE_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:

            self.path = str(self.mw.lineEditRadioTXInfo.text()) 
            print "textfile" , str(self.mw.lineEditRadioTXInfo.text()) 
            base=os.path.basename(self.path)
            dict = {}
            dict['device_control'] = 'FILE_DELETE_ID'
            dict['value'] = "/frt/"+base
        
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            
            
            
            self.on_pushButtonSendlData()
        pass
    def on_pushButtonGetRadioConfigureValue(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'DYNAMIC_VALUE_REQ'
            root = self.mw.treeWidgetDeviceConfigureIDList.invisibleRootItem()
            child_count = root.childCount()
            self.l = []
            for i in range(child_count):
                item = root.child(i)
                check = item.checkState(0)
                name = str(item.text(1))
                id =  int(str(item.text(2)))
                if check ==2:
                    self.l.append({"id": id ,"name":name})
                   
            
            print self.l
            dict['dynamicReq'] =  self.l
            
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            pass
    def on_pushButtonGetRadioMetricValue(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'FIXED_VALUE_REQ'
            root = self.mw.treeWidgetMetritcIDList.invisibleRootItem()
            child_count = root.childCount()
            self.l = []
            for i in range(child_count):
                item = root.child(i)
                check = item.checkState(0)
                name = str(item.text(1))
                id =  int(str(item.text(2)))
                if check ==2:
                    self.l.append({"id": id ,"name":name,"is_sensor":False})
                   
            
            print self.l
            dict['fixedReq'] =  self.l
            
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            pass
            
    def on_pushButtonGetRadioSensorValue(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'FIXED_VALUE_REQ'
            root = self.mw.treeWidgetSensorIDList.invisibleRootItem()
            child_count = root.childCount()
            self.l = []
            for i in range(child_count):
                item = root.child(i)
                check = item.checkState(0)
                name = str(item.text(1))
                id =  int(str(item.text(2)))
                if check ==2:
                    self.l.append({"id": id ,"name":name,"is_sensor":True})
                   
            
            print self.l
            dict['fixedReq'] =  self.l
            
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            pass
        
        
    
        
    def on_pushButtonRadioFileUpload(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setFilter(" files (*.*)")
            filenames = QStringList()
            self.showProgressBar = True
            if dlg.exec_():
                filenames= dlg.selectedFiles()
                self.path = str(filenames[0])

            self.mw.lineEditRadioTXInfo.setText (self.path)
            print "textfile" , str(self.mw.lineEditRadioTXInfo.text()) 
            self.buffer_size = os.path.getsize(self.path)
            base=os.path.basename(self.path)
            dict = {}
            dict['device_control'] = 'FILE_OPEN_ID'
            dict['value'] = "/frt/"+base
            dict['mode'] = 0x11 #FILE_WRITE
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            
            
            progress = QProgressDialog('Uploading Bytes ', 'Cancel', 0, 200, self.mw)
            progress.setWindowTitle("File Uploading start")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            progress.setValue(0)
            progress.setMinimum(0)
            progress.setMaximum(self.buffer_size)
            total_len =0
            print "fileopen===================="
            index = 0
            id =1
            with open(self.path, "rb") as target_file:
                while True:
                    buffer = target_file.read(128)
                    print "read"
                    #print buffer
                    #if buffer !=None:
                    waitt_time = 2
                    if index%10==0:
                          waitt_time=10
                    self.build_file_write(id,buffer,waitt_time)
                    if not buffer:
                        break 
                    #time.sleep(0.05)
                    app.processEvents()
                    total_len = total_len + len(buffer)
                    progress.setValue(total_len)
                    #if index > 100:
                    #    break 
                    index = index +1
                    print " sent size" , index*128/1024.0
            print ">>>>>>>>>>>>>>>>>>>> close"
            target_file.close()    
            
            

            dict['device_control'] = 'FILE_CLOSE_ID'
            dict['id'] = 1
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            self.on_pushButtonSendlData()
            
            
            
        pass
    def on_pushButtonRadioFWupdate(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_FWUP
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'FWUP'
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            
        self.on_pushButtonSendlData()
    def on_pushButtonRadioDeviceReset(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_DEVICE_RESET
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'DEVICE_RESET'
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            
        self.on_pushButtonSendlData()
   
    def on_pushButtonRadioGetSerial(self):
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_GET_SERIAL
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'GET_SERIAL'
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            
        self.on_pushButtonSendlData()
        
    def on_pushButtonRadioGetTime(self):    
        if self.isLORA:
            control={}
            control['device_control']= self.loralib.LORA_RADIO_DEVICE_CONTROL_GET_RTC
            aResult=self.loralib.buildDeviceControlRequest(control)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        else:
            dict = {}
            dict['device_control'] = 'GET_RTC'
            aResult=self.vonxcRadioLib.serialize(dict)
            self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
            
        self.on_pushButtonSendlData()    
    
    def on_pushButtonGetVersion(self):
        dict = {}
        dict['device_control'] = 'VERSION_ID'
        aResult = self.vonxcRadioLib.serialize(dict)
        self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.radioReceved = False
        (rc, mid) = self.client.publish(self.topic_tx,binascii.a2b_hex(str(payload )),qos=0)
        self.mid =  mid     
        
    def on_pushButtonSendlData(self):
        text = self.mw.lineEditSUBTOPIC.text()
        
        payload = self.mw.lineEditRadioVirtaulData.text()
        size = len(payload)            
        self.client.publish(self.topic_tx,binascii.a2b_hex(str(payload )))
        pass
    def on_publish(self,client,userdata,result): 
        print("data published " + str(result))

        if self.mid == result:
            self.radioOnPublished = True
        pass    
        
    def build_file_write(self,id,payload, wait_time):
        dict = {}
        dict['device_control'] = 'FILE_WRITE_ID'
        dict['value'] =payload
        dict['id'] = id
        aResult = self.vonxcRadioLib.serialize(dict)
        self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.fwReceive = False
        self.pubTime = time.time()
        self.on_pushButtonSendlData()
        
        index = 0
        while True:
       
              time.sleep(0.01)
              index  = index +1
              if self.fwReceive  == True:
                 break
              if index > wait_time:
                break
              app.processEvents()
      
        return aResult
    
    def build_file_read(self,id,size, pos, wait_time):
        dict = {}
        dict['device_control'] = 'FILE_READ_ID'
        dict['length'] =size
        dict['pos'] =pos
        dict['id'] = id
        aResult = self.vonxcRadioLib.serialize(dict)
        self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.frReceive = False
        self.on_pushButtonSendlData()
        
        index = 0
        returnValeue = None 
        while True:
       
              time.sleep(0.01)
              index  = index +1
              if self.frReceive  == True:
                returnValeue = self.frBytes
                break
              if index > wait_time:
                break
              app.processEvents()
      
        return returnValeue
            
    def on_pushButtonNetConnect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        text = self.mw.lineEditSUBTOPIC.text()
        self.topic_tx = "vonxc/"+str(text)+"/rx" 
        self.topic_rx = "vonxc/"+str(text)+"/tx" 
        
        self.client.connect("221.140.5.186", 1883, 60)
        self.vonxcRadioLib = vonxclib.ProtobufFormatter()
        self.client.loop_start()
    def on_connect(self, client, userdata, flagdict_, rc):
      print ("Connected with result coe " + str(rc))
      text = self.mw.lineEditSUBTOPIC.text()
      payload = self.mw.lineEditRadioVirtaulData.text()
      client.subscribe(self.topic_rx)

    def callback_result(self,message):  
    
        if message.type == vonxc_pb2.RadioVehicleMessage.DEVICE_CONTROL_RESP:
            if message.device_control_response.type == vonxc_pb2.DeviceControlRequest.VERSION_ID:
                self.mw.lineEditRadioVersion.setText( str(message.device_control_response.version))
                
            if  message.device_control_response.type == vonxc_pb2.DeviceControlRequest.GET_SERIAL:
                 self.mw.lineEditRadioRxInfo.setText(str(message.device_control_response.getSerial.value))
            if  message.device_control_response.type == vonxc_pb2.DeviceControlRequest.GET_RTC:
            
                time=message.device_control_response.uintvalue
                 
                timstring = datetime.datetime.fromtimestamp(
                 int(time)
                ).strftime('%Y-%m-%d %H:%M:%S')
                self.mw.lineEditRadioRxInfo.setText(timstring)
                
            if  message.device_control_response.type == vonxc_pb2.DeviceControlRequest.FILE_WRITE_ID:
                self.fwReceive = True
                
            if  message.device_control_response.type == vonxc_pb2.DeviceControlRequest.FILE_READ_ID:
                self.frReceive = True    
                self.frBytes = message.device_control_response.fread.value
                
        if message.type == vonxc_pb2.RadioVehicleMessage.RADIO_FIXED_VALUE:
            print "message.fixedValueMap.valueList" 
            result = ''
            for x in message.fixedValueMap.valueList:
                print "value List" , x
                uint = str(x.id)  + ": " + str(x.numeric_value) + ", "
                result = result +str(uint)
            
            self.mw.lineEditRadioRxInfo.setText(str(result))
                
        if message.type == vonxc_pb2.RadioVehicleMessage.RADIO_DYNAMIC_VALUE:
            print "message.dynmaicValueMap.valueList"
            result = ''
            for x in message.dynamicValueMap.valueList:
                print "=============> value List x.type " , x.type
                if x.type == vonxc_pb2.DynamicField.STRING:
                    uint = str(x.id)  + ": " + str(x.string_value) + ", "
                if x.type == vonxc_pb2.DynamicField.BYTE:
                    uint = str(x.id)  + ": " + str(binascii.hexlify(x.byte_value)) + ", "    
                    
                result = result +str(uint)
            self.mw.lineEditRadioRxInfo.setText(str(result))
      
    def on_message(self,client, userdata, msg):
        l =[]
        print "Topic: ", msg.topic + '\nMessage: ' + binascii.hexlify(bytearray((msg.payload)))
        hex_string = binascii.hexlify(bytearray((msg.payload)))
        parsed_result=  self.vonxcRadioLib.parse_next_message(msg.payload)
        timstring = datetime.datetime.fromtimestamp(
                    int(time.time())
                ).strftime('%Y-%m-%d %H:%M:%S')
        tx_string = 'RX'
        aREturnMsg =   str(parsed_result)
        aREturnMsg =  aREturnMsg.replace('\n','')
        aREturnMsg =  aREturnMsg.replace('\r','')
                   
        aRow = [timstring,tx_string,str(hex_string),str(aREturnMsg)]
        l.append (QtGui.QTreeWidgetItem(aRow))         
        self.mw.treeWidgetRadioPacketLog.addTopLevelItems(l)
        self.radioReceved = True
        print "timegap ", time.time() - self.pubTime
        self.callback_result(parsed_result)
        '''
        if  parsed_result.type ==  vonxc_pb2.RadioVehicleMessage.DEVICE_CONTROL_RESP:
            if parsed_result.device_control_response.type == vonxc_pb2.DeviceControlRequest.VERSION_ID:
                self.mw.lineEditRadioVersion.setText( str(parsed_result.device_control_response.version))
        if  parsed_result.type ==  vonxc_pb2.RadioVehicleMessage.DEVICE_CONTROL_RESP: 
            if parsed_result.device_control_response.type == vonxc_pb2.DeviceControlRequest.FILE_READ_ID:        
                    self.fwReceive = True
        '''
    def build_file_open(self, filename, mode):
        dict = {}
        dict['device_control'] = 'FILE_OPEN_ID'
        dict['value'] = filename
        dict['mode'] = mode #FILE_WRITE
        self.pubTime = time.time()
        aResult = self.vonxcRadioLib.serialize(dict)
        self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.radioReceved = False
        (rc, mid) = self.client.publish(self.topic_tx,binascii.a2b_hex(str(payload )),qos=2)
        self.mid =  mid 
        while self.radioReceved  == False:
              time.sleep(0.01)
              break

        return aResult
    
    def on_pushButtonBuildConfigFileChoose(self):
    
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(" files (*.*)")
        filenames = QStringList()
        self.showProgressBar = True

        if dlg.exec_():
            filenames= dlg.selectedFiles()
            self.path = str(filenames[0])

        self.mw.lineEditRadioFileInfo.setText (self.path)
        print "textfile" , str(self.lineEditRadioFileInfo.text()) 

    def build_file_write(self,id,payload, wait_time):
        dict = {}
        dict['device_control'] = 'FILE_WRITE_ID'
        dict['value'] =payload
        dict['id'] = id
        aResult = self.vonxcRadioLib.serialize(dict)
        self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
        payload = self.mw.lineEditRadioVirtaulData.text()
        self.fwReceive = False
        self.pubTime = time.time()
        infot =self.client.publish(self.topic_tx,binascii.a2b_hex(str(payload )),qos=2)
        infot.wait_for_publish()
        index = 0
        while True:
       
              time.sleep(0.01)
              index  = index +1
              if self.fwReceive  == True:
                 break
              if index > wait_time:
                break
              app.processEvents()
      
        return aResult
    
    def build_file_close(self,id):
         dict = {}
         dict['device_control'] = 'FILE_CLOSE_ID'
         dict['id'] = id
         self.pubTime = time.time()
         aResult = self.vonxcRadioLib.serialize(dict)
         self.mw.lineEditRadioVirtaulData.setText(binascii.hexlify(aResult))
         payload = self.mw.lineEditRadioVirtaulData.text()
         self.radioReceved =False
         (rc, mid) = self.client.publish(self.topic_tx,binascii.a2b_hex(str(payload )),qos=2)
         self.mid =  mid 
         while self.radioReceved  == False:
              time.sleep(0.01)
              break
         return aResult   
         
        

class ManagerWindow(BaseWindow):
    def __init__(self):
        super(ManagerWindow, self).__init__()
   

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    windows = ManagerWindow()
    windows.load_ui('mqttserver.ui')
    windows.show()
    sys.exit(app.exec_())