import struct
import binascii
import time

class LoraParser():
    LORA_VERSION=1

    LORA_RADIO_VEHICLE_MESSAGE_BUS = 1
    LORA_RADIO_VEHICLE_MESSAGE_SIMPLE = 2
    LORA_RADIO_VEHICLE_MESSAGE_DIAGNOSTIC_COMMAND = 3
    LORA_RADIO_VEHICLE_MESSAGE_DEVICE_CONTROL_REQ = 4
    LORA_RADIO_VEHICLE_MESSAGE_DIAGNOSTIC_RESPONSE = 5
    LORA_RADIO_VEHICLE_MESSAGE_DEVICE_CONTROL_RESP = 6
    LORA_RADIO_VEHICLE_MESSAGE_DYNAMIC_VALUE = 7
    LORA_RADIO_VEHICLE_MESSAGE_FIXED_VALUE = 8
    LORA_RADIO_VEHICLE_MESSAGE_POSITION_VALUE = 9
    LORA_RADIO_VEHICLE_MESSAGE_TRIP_VALUE = 10
    
    
    
    
    
    
    
    
    LORA_RADIO_DEVICE_CONTROL_VERSION_ID = 1
    LORA_RADIO_DEVICE_CONTROL_DEVICE_ID = 2
    LORA_RADIO_DEVICE_CONTROL_GET_SERIAL = 3
    LORA_RADIO_DEVICE_CONTROL_FILE_OPEN_ID = 4
    LORA_RADIO_DEVICE_CONTROL_FILE_WRITE_ID = 5
    LORA_RADIO_DEVICE_CONTROL_FILE_READ_ID = 6
    LORA_RADIO_DEVICE_CONTROL_FILE_SEEK_ID = 7
    LORA_RADIO_DEVICE_CONTROL_FILE_CLOSE_ID = 8
    LORA_RADIO_DEVICE_CONTROL_CLI_CHANGE = 9
    LORA_RADIO_DEVICE_CONTROL_FWUP = 10
    LORA_RADIO_DEVICE_CONTROL_SET_RTC = 11
    LORA_RADIO_DEVICE_CONTROL_DEVICE_RESET = 12
    LORA_RADIO_DEVICE_CONTROL_GET_RTC = 19
    LORA_RADIO_DEVICE_CONTROL_BEEP = 20

    LORA_RADIO_DEVICE_CONTROL_FILE_DELETE_ID = 14
    LORA_RADIO_DEVICE_CONTROL_FILE_LIST_GET_COUNT = 15
    LORA_RADIO_DEVICE_CONTROL_FILE_LIST_GET_ITEM = 16

    LORA_RADIO_DEVICE_CONTROL_SFW_VERSION = 30
    LORA_RADIO_DEVICE_CONTROL_SFW_PATCH = 31

    LORA_RADIO_DEVICE_CONTROL_DIAG_STOP = 51
    LORA_RADIO_DEVICE_CONTROL_DIAG_START = 52

    LORA_RADIO_DEVICE_CONTROL_GET_SENSOR_COUNT = 61
    LORA_RADIO_DEVICE_CONTROL_GET_SENSOR_ITEM = 62
    LORA_RADIO_DEVICE_CONTROL_GET_SENSOR_VALUE = 63
    LORA_RADIO_DEVICE_CONTROL_SET_SENSOR_VALUE = 64

    LORA_RADIO_DEVICE_CONTROL_GET_METRIC_COUNT = 75
    LORA_RADIO_DEVICE_CONTROL_GET_METRIC_ITEM = 76
    LORA_RADIO_DEVICE_CONTROL_GET_METRIC_VALUE = 77
    LORA_RADIO_DEVICE_CONTROL_SET_METRIC_VALUE = 78

    LORA_RADIO_DEVICE_CONTROL_GET_DEVICE_CONFIGURE_COUNT = 81
    LORA_RADIO_DEVICE_CONTROL_GET_DEVICE_CONFIGURE_ITEM = 82
    LORA_RADIO_DEVICE_CONTROL_GET_DEVICE_CONFIGURE_VALUE = 83
    LORA_RADIO_DEVICE_CONTROL_SET_DEVICE_CONFIGURE_VALUE = 84

    LORA_RADIO_DEVICE_CONTROL_REQUEST_CHALLENGE = 91
    LORA_RADIO_DEVICE_CONTROL_REQUEST_AUTH = 92
    LORA_RADIO_DEVICE_CONTROL_CHECK_AUTH = 93
    LORA_RADIO_DEVICE_CONTROL_CHANGE_PASSWORD = 94
    
        
    
    def getLoraValueID(self, id):
        print bin(id)
        return id
        
    
    def getSensorList(self):
        a=  [
        { 'name':'lora_value_sensor_engine_speed', 'id':1},
        { 'name':'lora_value_sensor_vehicle_speed', 'id':2},
        { 'name':'lora_value_sensor_engine_load', 'id':3}, 
        { 'name':'lora_value_sensor_engine_coolant_temperature', 'id':4},
        { 'name':'lora_value_sensor_barometric_pressure', 'id':5},
        { 'name':'lora_value_sensor_commanded_throttle_position', 'id':6}, 
        { 'name':'lora_value_sensor_fuel_level', 'id':7},
        { 'name':'lora_value_sensor_intake_air_temperature', 'id':8},
        { 'name':'lora_value_sensor_intake_manifold_pressure', 'id':9}, 
        { 'name':'lora_value_sensor_running_time', 'id':10},
        { 'name':'lora_value_sensor_throttle_position', 'id':11},
        { 'name':'lora_value_sensor_fuel_pressure', 'id':12}, 
        { 'name':'lora_value_sensor_mass_airflow', 'id':13},
        { 'name':'lora_value_sensor_accelerator_pedal_position', 'id':14},
        { 'name':'lora_value_sensor_ethanol_fuel_percentage', 'id':15},
        { 'name':'lora_value_sensor_engine_oil_temperature', 'id':16},
        { 'name':'lora_value_sensor_engine_torque', 'id':17},
        { 'name':'lora_value_sensor_lat_degree', 'id':18},         
        { 'name':'lora_value_sensor_lon_degree', 'id':19},
        { 'name':'lora_value_sensor_alt_meter', 'id':20},
        { 'name':'lora_value_sensor_yaw', 'id':21}, 
        { 'name':'lora_value_sensor_roll', 'id':22},
        { 'name':'lora_value_sensor_pitch', 'id':23},
        { 'name':'lora_value_sensor_x_accel', 'id':24}, 
        { 'name':'lora_value_sensor_y_accel', 'id':25},
        { 'name':'lora_value_sensor_z_accel', 'id':26},
        { 'name':'lora_value_metric_engine_on_time', 'id':27}, 
        { 'name':'lora_value_metric_engine_off_time', 'id':28},
        { 'name':'lora_value_metric_speed_on_time', 'id':29},
        { 'name':'lora_value_metric_speed_off_time', 'id':30}, 
        { 'name':'lora_value_metric_mtrip_airflow', 'id':31},
        { 'name':'lora_value_metric_mtrip_mfold_airflow', 'id':32},
        { 'name':'lora_value_metric_mtrip_on_time', 'id':33}, 
        { 'name':'lora_value_metric_mtrip_off_time', 'id':34},
        { 'name':'lora_value_metric_mtrip_duration', 'id':35},
        { 'name':'lora_value_metric_mtrip_distance', 'id':36},
        { 'name':'lora_value_metric_gps_ttff', 'id':37},
        { 'name':'lora_value_metric_radio_ttfc', 'id':38},
        { 'name':'lora_value_metric_boot_timegap', 'id':39},         
        { 'name':'lora_value_metric_radio_last_stime', 'id':40},
        { 'name':'lora_value_metric_radio_byte_sent', 'id':41},
        { 'name':'lora_value_metric_radio_byte_recv', 'id':42},
        { 'name':'lora_value_metric_radio_last_rtime', 'id':43}
        ]
    def getValueList(self):
        a=  [
        { 'name':'lora_value_reset', 'id':1},
        { 'name':'lora_value_rtc', 'id':2},         
        { 'name':'lora_value_beep', 'id':3},
        { 'name':'lora_value_cfirm_trip', 'id':4},
        { 'name':'lora_value_sensor_request', 'id':5},
        { 'name':'lora_value_metric_request', 'id':6}            
        ]
        return a
    def getConfigList(self):
        a=  [
        { 'name':'lora_config_set_serial', 'id':1},
        { 'name':'lora_config_get_serial', 'id':2}, 
        { 'name':'lora_config_get_vin', 'id':3}, 
        { 'name':'lora_config_fwrite', 'id':4},
        { 'name':'lora_config_fread', 'id':5},
        { 'name':'lora_config_finfo', 'id':6},     
        { 'name':'lora_config_diag_req', 'id':7},
        { 'name':'lora_config_diag_resp', 'id':8}, 
        { 'name':'lora_config_bus_req', 'id':9},
        { 'name':'lora_config_bus_rsp', 'id':10}, 
        { 'name':'lora_config_sensor_req', 'id':11},
        { 'name':'lora_config_metric_req', 'id':12}  
        ]

        return a

    def buildPacketFromValue(self,valueList):
        packet= bytes()
        packet = packet + bytes(chr(self.LORA_VERSION))
        packet = packet + bytes(chr(self.LORA_VALUE_PACKET_TYPE))
        packet = packet +  struct.pack("I",time.time())         
        packet = packet + bytes(0)
        packet = packet + bytes(chr(len(valueList)))
        for x in valueList:
            id = x['id']
            value = x['value']
            packet = packet + struct.pack("H",id)
            packet = packet + struct.pack("B",0)           
            packet = packet + struct.pack("I",value)
        len_diff = 64 - len(packet)
        packet += "\0"*len_diff
        
        return packet
    
    def buildDeviceControlRequest(self,control):
        packet= bytes()
        packet = packet + bytes(chr(self.LORA_VERSION))
        packet = packet + bytes(chr(self.LORA_RADIO_VEHICLE_MESSAGE_DEVICE_CONTROL_REQ))
        packet = packet +  struct.pack("I",time.time())

        id = control['device_control']         
        packet = packet +  struct.pack("B",id)

        len_diff = 64 - len(packet)
        packet += "\0"*len_diff
        
        return packet
        
        
        
    def buildPacketFromForFileWrite(self,name,offset,payload):
        packet= bytes()
        packet = packet + bytes(chr(self.LORA_VERSION))
        packet = packet + bytes(chr(self.LORA_CONFIG_PACKET_TYPE))
        packet = packet +  struct.pack("I",time.time())  
        len_name = len(name)
        if len_name < 8:
            len_diff  = 8 - len_name
            name += "\0"*len_diff
        len_payload = len(payload)    
        packet = packet +  bytes(chr(4)) #file write
        packet = packet +  name[0:8]
        packet = packet +  struct.pack("I",len_payload)
        packet = packet +  struct.pack("I",offset)
        packet = packet +  bytes(payload)

        alen_diff = 64 - (len(packet))  
        
        packet += "\0"*alen_diff
        print binascii.hexlify(packet)
        return packet    

    
    def buildPacketFromForDiagRequest(self,duration,chained,bus, freq_time,diagRequest):
        packet= bytes()
        packet = packet + bytes(chr(self.LORA_VERSION))
        packet = packet + bytes(chr(self.LORA_CONFIG_PACKET_TYPE))
        packet = packet +  struct.pack("I",time.time())  
         
        packet = packet +  bytes(chr(7)) #diag rquest
        packet = packet +  bytes(chr(duration)) 
        packet = packet +  bytes(chr(chained)) 
        packet = packet + bytes(chr(bus)) 
        packet = packet +  bytes(chr(freq_time)) 
        packet = packet + struct.pack("B",len(diagRequest))
        for x in diagRequest:
            value = x['id']
            packet = packet + struct.pack("I",value)
            value = x['mode']
            packet = packet + struct.pack("B",value)
            value = x['pid']
            packet = packet + struct.pack("B",value)
            value = x['payload_length']
            packet = packet + struct.pack("B",value)
            value = x['payload']
            if len(value)<4:
                alen_diff = 4 - (len(value)) 
                value += "\0"*alen_diff
                
            packet = packet + value[0:]
            
        alen_diff = 64 - (len(packet)) 
        packet += "\0"*alen_diff
        print binascii.hexlify(packet)
        return packet

        
    def parser(self,packet):
        version = int(packet[0])
        type = int(packet[1])
        ts= struct.unpack('<I', bytearray( packet[2:6]))[0]
        print "type ==============>" , type
        print "version ==============>" , version
        print "ts ==============>" , ts
        
        if type == self.LORA_RADIO_VEHICLE_MESSAGE_FIXED_VALUE:
            print 'LORA_RADIO_VEHICLE_MESSAGE_FIXED_VALUE'
            returnValue = {}
            size = int(packet[6])
            valuelist=[]
            packet_index = 7 
            returnValue['name']= " LORA_RADIO_VEHICLE_MESSAGE_FIXED_VALUE "
            print  "size", size 
            for x in range(0,size):
                type= int(packet[packet_index])
                packet_index = packet_index +1
                id =  struct.unpack('<H',(packet[packet_index:packet_index+2]))[0]
                packet_index = packet_index +2
                ts_offset =  int(packet[packet_index])
                packet_index = packet_index +1
                value =  struct.unpack('<f',packet[packet_index:packet_index+4])[0]
                packet_index = packet_index +4
                valueitem={} 
                valueitem['type'] = type 
                valueitem['id'] = "0x%04X" % id
                valueitem['ts_offset'] = ts_offset
                valueitem['value'] = value
                valuelist.append(valueitem)                
                print  type, id , ts_offset , value 
                
            returnValue['valuelist'] = valuelist
            print returnValue
            return returnValue
        if type == self.LORA_RADIO_VEHICLE_MESSAGE_DYNAMIC_VALUE:
            print 'LORA_RADIO_VEHICLE_MESSAGE_DYNAMIC_VALUE'
            returnValue = {}
            packet_index = 6
            id =  struct.unpack('<H',(packet[packet_index:packet_index+2]))[0]
            packet_index = packet_index +2
            type =   int(packet[packet_index])
            packet_index = packet_index +1
            ts_offset =  int(packet[packet_index])
            packet_index = packet_index +1
            size  =  int(packet[packet_index])
            packet_index = packet_index +1
            returnValue['id']  = id 
            
            print "id", id , " type", type, "size", size
            
            if type ==0:
                 returnValue['value'] =  str(packet[packet_index: packet_index +size])
            if type ==1:
                 returnValue['value'] =   binascii.a2b_hex(packet[packet_index:packet_index +size])

            returnValue['name']= "LORA_RADIO_VEHICLE_MESSAGE_DYNAMIC_VALUE "
            print  "size", size 
            
            print returnValue
            return returnValue    
        if type == self.LORA_RADIO_VEHICLE_MESSAGE_POSITION_VALUE:
            print 'LORA_RADIO_VEHICLE_MESSAGE_POSITION_VALUE'
            returnValue = {}
            packet_index = 6
            lat =  struct.unpack('<f',(packet[packet_index:packet_index+4]))[0]
            returnValue['lat']=lat
            packet_index = packet_index +4 
            
            lon =  struct.unpack('<f',(packet[packet_index:packet_index+4]))[0]
            returnValue['lon']=lat
            packet_index = packet_index +4 
            
            size =  int(packet[packet_index])
            packet_index = packet_index +1 
            returnValue['size']=size
                
            poistionlist=[]
            print "lat", lat , " lon", lon, "size", size
                     
            for x in range(0,size):
                postionitem={}  
                time_offset = int(packet[packet_index])
                packet_index = packet_index +1 
                lat_offset =  int(packet[packet_index])
                packet_index = packet_index +1 
                lon_offset =  int(packet[packet_index])
                packet_index = packet_index +1 
                print time_offset , lat_offset , lon_offset
                postionitem['time_offset'] = time_offset
                postionitem['lat_offset'] = lat_offset
                postionitem['lon_offset'] = lon_offset
                poistionlist.append(postionitem)
            
            returnValue['name']= "LORA_RADIO_VEHICLE_MESSAGE_POSITION_VALUE "   
            returnValue['poistionlist'] = poistionlist
        
            return returnValue    
        if type == self.LORA_RADIO_VEHICLE_MESSAGE_TRIP_VALUE:
            print 'LORA_RADIO_VEHICLE_MESSAGE_TRIP_VALUE'
            returnValue = {}
            packet_index = 6
            parsedValue = struct.unpack('<IBHBffffBfHIHBBB', bytearray(packet_index[6:]))
            returnValue['timestamp']=parsedValue[0]
            returnValue['encrypt']=parsedValue[1]
            returnValue['trip_id']=parsedValue[2]
            returnValue['type']=parsedValue[3]
            returnValue['start_lat']=parsedValue[4]
            returnValue['start_lon']=parsedValue[5]
            returnValue['end_lat']=parsedValue[6]
            returnValue['end_lon']=parsedValue[7]    
            returnValue['airFlowType']=parsedValue[8]
            returnValue['airFlow']=parsedValue[9] 
            returnValue['max_speed']=parsedValue[10] 
            returnValue['distance_km']=parsedValue[11] 
            returnValue['duration']=parsedValue[12] 
            returnValue['engineOilTemp']=parsedValue[13] 
            returnValue['ParkVolt']=parsedValue[14]
            returnValue['name']= "LORA_RADIO_VEHICLE_MESSAGE_TRIP_VALUE "  
            
        if type == self.LORA_VALUE_PACKET_TYPE:
            print 'LORA_VALUE_PACKET_TYPE'
            returnValue = {}
            parsedValue = struct.unpack('<BBIBB56B', bytearray(packet))
            returnValue['version']=parsedValue[0]
            returnValue['type']=parsedValue[1]
            returnValue['timestamp']=parsedValue[2]
            returnValue['encrypt']=parsedValue[3]
            returnValue['size']=parsedValue[4]
            valuelist=[]
            index =5
    
            for x in range(0,int(parsedValue[4])):
                print "index", index 
                valueitem={}  
                item_parsed = struct.unpack('<HBI', bytearray(parsedValue[index:index+7]))
                id = item_parsed[0]
                ts_offset = item_parsed[1]
                value = item_parsed[2]
        
        
                index = index + 7
                print id , value
                valueitem['id'] = "0x%04X" % id
                valueitem['value'] = value
                valueitem['ts_offset'] = ts_offset
                valuelist.append(valueitem)
               
            returnValue['valuelist'] = valuelist
       
            return returnValue

