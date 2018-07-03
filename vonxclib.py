from __future__ import absolute_import

import binascii
import numbers
import logging
import time

import google.protobuf.message
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal import encoder

from  vonxc import vonxc_pb2

class ProtobufFormatter(object):
    MAX_PROTOBUF_MESSAGE_LENGTH = 512
    def __init__(self):
        pass
        
    def parse_next_message(self, from_u):
        message = None
       
        message_data = ""
        message_length, message_start = _DecodeVarint(from_u, 0)
        if message_start + message_length > len(from_u):
            print "size error"
            return 
        message_data = from_u[message_start:message_start +
                    message_length]
                    
        print "vonxc returnvalue  parse_next_message " ,binascii.hexlify(message_data)            
        message = self.deserialize(message_data)
        return message         
                    
        # 1. decode a varint from the top of the stream
        # 2. using that as the length, if there's enough in the buffer, try and
        #       decode try and decode a VehicleMessage after the varint
        # 3. if it worked, great, we're oriented in the stream - continue
        # 4. if either couldn't be parsed, skip to the next byte and repeat
        

    @classmethod
    def deserialize(self, data):
        message = vonxc_pb2.RadioVehicleMessage()
        print "vonxc returnvalue " ,binascii.hexlify(bytearray(data))
        try:
            message.ParseFromString(data)
        except google.protobuf.message.DecodeError as e:
            print "decode error"
            pass
        except UnicodeDecodeError as e:
            print("Unable to parse protobuf: %s", e)
            #print "decode error"
        else:
            return message

    @classmethod
    def serialize(cls, data):
        protobuf_message =  cls._dict_to_protobuf(data).SerializeToString()
        delimiter = encoder._VarintBytes(len(protobuf_message))
        return delimiter + protobuf_message
    @classmethod
    def _command_string_to_protobuf(self, command_name):
        pass

    @classmethod
    def getDeviceControlList(self):
        list = []
        desc = vonxc_pb2.DeviceControlRequest.Type.DESCRIPTOR
        for (k,v) in desc.values_by_name.items():
            dict={}
            dict['name'] = k
            list.append(dict)   
        return list
       
    @classmethod
    def getSensorList(self):
        list = []
        desc = vonxc_pb2.RadioVehicleMessage.SENSOR_ID.DESCRIPTOR
        for (k,v) in desc.values_by_name.items():
            dict={}
            #print k, v.number
            dict['name'] = str(k)
            dict['id'] = v.number
            list.append(dict)   
        return list
    @classmethod
    def getMetricList(self):
        list = []
        desc = vonxc_pb2.RadioVehicleMessage.METRIC_ID.DESCRIPTOR
        for (k,v) in desc.values_by_name.items():
            dict={}
            #print k, v.number
            dict['name'] = str(k)
            dict['id'] = v.number
            list.append(dict)   
        return list  
    @classmethod
    def getDeviceConfigureList(self):
        list = []
        desc = vonxc_pb2.RadioVehicleMessage.DEVICE_CONFIGURE_ID.DESCRIPTOR
        for (k,v) in desc.values_by_name.items():
            dict={}
            #print k, v.number
            dict['name'] = str(k)
            dict['id'] = v.number
            list.append(dict)   
        return list      
    @classmethod
    def _dict_to_protobuf(cls, data):
        message = vonxc_pb2.RadioVehicleMessage()
        message.version = vonxc_pb2.RadioVehicleMessage.VERSION_1_0
        message.timestamp = int(time.time())

        if 'device_control' in data:
            message.type = vonxc_pb2.RadioVehicleMessage.DEVICE_CONTROL_REQ
            command= data['device_control']
            if command =='VERSION_ID':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.VERSION_ID
            if command =='FWUP':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FWUP
            if command =='GET_SERIAL':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.GET_SERIAL
            if command =='DEVICE_RESET':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.DEVICE_RESET
            if command =='GET_RTC':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.GET_RTC
            
            if command =='FILE_READ_ID':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FILE_READ_ID
                message.device_control_request.fread.value = data["length"]
                message.device_control_request.fread.offset= data["pos"]
                message.device_control_request.fread.id= data["id"]
            if command =='FILE_OPEN_ID':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FILE_OPEN_ID
                name = data["value"]
                mode = data["mode"]
                message.device_control_request.fopen.value = name
                message.device_control_request.fopen.mode = mode
            if command =='FILE_WRITE_ID':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FILE_WRITE_ID
                bytestream = data["value"]
                id = data["id"]
                message.device_control_request.fwrite.value = bytestream
                message.device_control_request.fwrite.id = id
            if command =='FILE_CLOSE_ID':
                id = data["id"]
                message.device_control_request.fclose.id = id
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FILE_CLOSE_ID
            if command =='FILE_DELETE_ID':
                name = data["value"]
                message.device_control_request.fdelete.value = name
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FILE_DELETE_ID
            if command =='FIXED_VALUE_REQ':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.FIXED_VALUE_REQ
                
                fixedReq = data["fixedReq"] 
         
                l = []
                for x in fixedReq:
                    print x 
                    aValue = vonxc_pb2.FixedValue()
                    aValue.id =x['id']
                    aValue.isSensor = x['is_sensor']
                    print "aValue" , aValue
                    l.append(aValue)
                   
                  
                print "l==================" , l
                message.device_control_request.fixedReq.valueList.extend(l)
                print message.device_control_request.fixedReq.valueList 
            if command =='DYNAMIC_VALUE_REQ':
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.DYNAMIC_VALUE_REQ
                
                dynamicReq = data["dynamicReq"] 
               
                l = []
                for x in dynamicReq:
                    print x 
                    aValue = vonxc_pb2.DynamicField()
                    aValue.id =x['id']
                    print "aValue" , aValue
                    l.append(aValue)
                   
                  
                print "l==================" , l
                message.device_control_request.dynamicReq.valueList.extend(l)
                print message.device_control_request.dynamicReq.valueList   
            if command =='CLI_CHANGE':       
                message.device_control_request.type = vonxc_pb2.DeviceControlRequest.CLI_CHANGE
                
        print  binascii.hexlify(bytearray(message.SerializeToString()))
        
        
        return message
    def _protobuf_to_dict(cls, message):    
        parsed_message = {}
        print message
        if message is not None:
            if message.type == message.DEVICE_CONTROL_RESP :
                pass
            if message.type == message.RADIO_DYNAMIC_VALUE :
                pass
        return message