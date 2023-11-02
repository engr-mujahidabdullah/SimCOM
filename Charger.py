from Packet import Packet, ParsedPacket

class Charger(ParsedPacket):
     
    def __init__(self, ID = [0x00,0x00, 0x00, 0x01]):
        self.type = type = [0x02]
        self.ID = ID
        self.voltage_out = [0x00, 0x00]  # in Voltage        
        self.voltage_start = [0x00, 0x00]
        self.voltage_setpoint = [0x00, 0x00]
        self.voltage_over_th = [0x00, 0x00]
        self.current_out = [0x00, 0x00, 0x00, 0x00] # in milliAmps
        self.current_cutoff = [0x00, 0x00, 0x00, 0x00] 
        self.current_setpoint = [0x00, 0x00, 0x00, 0x00]
        self.current_fan_start = [0x00, 0x00, 0x00, 0x00]
        self.current_fan_stop = [0x00, 0x00, 0x00, 0x00]
        self.current_over_th = [0x00, 0x00, 0x00, 0x00] 
        self.temperature_amb = [0x00, 0x00] #in Celcius
        self.temperature_hs = [0x00, 0x00]
        self.temperature_fan_start = [0x00, 0x00]
        self.temperature_fan_stop = [0x00, 0x00]
        #self.temperature_cutoff = [0x00, 0x00]
        #self.temperature_restart = [0x00, 0x00]
        self.temperature_over_th = [0x00, 0x00]
        self.allow_charging = [0x00, 0x00]
        self.status = [0x00, 0x00, 0x00, 0x00]
    

    def charger_attributes(self):
        attributes = vars(self)  # Get all attributes of the class instance
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

    def response(self, data):
        data = self.process_packet(data)
        if(data.type == [0x00] and data.serial == [0x00,0x00,0x00, 0x00] and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
            
        if(data.type == self.type and data.serial == self.ID and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
            
        if(data.type == self.type and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
            
        if(data.type == [0x00] and data.serial == self.ID and data.cmd == [0x01,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
            
        if(data.type == self.type and data.serial == self.serial and data.cmd == [0x02, 0x00]):
            data = self.voltage_start + self.current_cutoff + self.temperature_fan_start + self.temperature_fan_stop + self.current_fan_start + self.current_fan_stop + self.current_over_th + self.voltage_over_th + self.temperature_over_th + self.voltge_setpoint + self.current_setpoint 
            return self._packet_(serial_no = self.ID, type = self.type, cmd = self.cmd, data = data, request=False)
            
        if(data.type == self.type and data.serial == self.serial and data.cmd == [0x03, 0x00]):
            data = self.allow_charging
            return self._packet_(serial_no = self.ID, type = self.type, cmd = self.cmd, data = data, request=False)

        else:
            print("invalid")
    

    def data_parser(self, cmd, data):
        index = 0
        if(cmd == [0x01, 0x00]):
            self.voltage_out = [data[index], data[index + 1]]
            index += 2
        
            self.current_out = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.temperature_amb = [data[index], data[index + 1]]
            index += 2

            self.temperature_hs = [data[index], data[index + 1]]
            index += 2

            self.status = [data[index], data[index + 1]]
            index += 2
            return 0

        if(cmd == [0x02, 0x00]):
            self.voltage_start = [data[index], data[index + 1]]
            index += 2
        
            self.current_cutoff = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.temperature_fan_start = [data[index], data[index + 1]]
            index += 2

            self.temperature_fan_stop = [data[index], data[index + 1]]
            index += 2

            self.current_fan_start = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.current_fan_stop = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4
            
            self.current_over_th = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4
        
            self.voltage_over_th = [data[index], data[index + 1]]
            index += 2

            self.temperature_over_th = [data[index], data[index + 1]]
            index += 2

            self.voltage_setpoint = [data[index], data[index + 1]]
            index += 2

            self.current_setpoint = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4
            return 0
        
        if(cmd == [0x03, 0x00]):
            self.allow_charging = [data[index], data[index + 1]]
            index += 2         
            return 0   

        else:
            return -1
