from data_check import CRC16
from Packet import Packet, ParsedPacket

class Battery(ParsedPacket):
    def __init__(self, type = [0xAA], ID = [0x12,0x34, 0x56, 0x78]):
        self.type = type
        self.ID = ID
        self.capacity = [0x00, 0x00, 0x00, 0x00]  # in milliampere-hours (mAh)
        self.temperature = [0x00, 0x00] # in Celcius 
        self.voltage = [0x00, 0x00]    # in volts (V)
        self.current = [0x00, 0x00, 0x00, 0x00]
        self.SoC = [0x00]
        self.SoH = [0x00]
        self.status = [0x00, 0x00, 0x00, 0x00]
        self.discharging_KWh = [0x00, 0x00, 0x00, 0x00]
        self.charging_KWh = [0x00, 0x00, 0x00, 0x00]
        self.discharging_time = [0x00, 0x00, 0x00, 0x00]
        self.charging_time = [0x00, 0x00, 0x00, 0x00]
        self.voltage_high = [0x00, 0x00]
        self.voltage_low = [0x00, 0x00]
        self.temperature_high = [0x00, 0x00]
        self.temperature_low = [0x00, 0x00]




    # Getters
    def get_ID(self):
        return self.ID

    def get_type(self):
        return self.type
    
    def get_capacity(self):
        return self.capacity

    def get_voltage(self):
        return self.voltage

    def get_current(self):
        return self.current
    
    def get_SoH(self):
        return self.voltage

    def get_SoC(self):
        return self.current

    # Setters
    def set_capacity(self, capacity):
        if capacity > 0:
            self.capacity = capacity
        else:
            print("Capacity must be a positive value.")

    def set_voltage(self, voltage):
        if voltage > 0:
            self.voltage = voltage
        else:
            print("Voltage must be a positive value.")

    def set_current(self, current):
        self.current = current

    def set_SoC(self, SoC):
        if SoC >= 0 & SoC <= 100:
            self.SoC = SoC
        else:
            print("SOC must be in a range")

    def set_SoH(self, SoC):
        if SoC >= 0 & SoC <= 100:
            self.SoC = SoC
        else:
            print("SOC must be in a range")


    def process_packet(self, data):
        return self.parse_received_packet(data)

    def response(self, data):
        data = self.process_packet(data)
        if(data.type == [0x00] and data.serial == [0x00,0x00,0x00, 0x00] and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
        
        if(data.type == [0x01] and data.serial == self.ID and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
        
        if(data.type == [0x01] and data.cmd == [0x00,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
        
        if(data.type == [0x00] and data.serial == self.ID and data.cmd == [0x01,0x00]):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)
        
        if(data.type == self.type and data.serial == self.serial and data.cmd == 0x1111):
            data = self.voltage + self.h_voltage + self.l_voltage + self.current + self.temperature + self.h_temperature + self.l_temperature + self.SoC + self.SoH + self.char_kwh + self.dis_kwh + self.char_time + self.dis_time + self.status
            return self._packet_(serial_no = self.ID, type = self.type, cmd = self.cmd, data = data, request=False)
        else:
            print("invalid")
 
    def parse_data(self, data):
        index = 0

        # Define lists to store the parsed data
        self.voltage = [data[index], data[index + 1]]
        index += 2

        self.current = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4

        self.temperature = [data[index], data[index + 1]]
        index += 2

        self.voltage_low = [data[index], data[index + 1]]
        index += 2

        self.voltage_high = [data[index], data[index + 1]]
        index += 2

        self.temperature_low = [data[index], data[index + 1]]
        index += 2

        self.charging_KWh = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4

        self.discharging_KWh = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4

        self.charging_time = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4

        self.discharging_time = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4

        self.status = [data[index], data[index + 1], data[index + 2], data[index + 3]]
        index += 4
