from data_check import CRC16
from Packet import Packet, ParsedPacket

class Battery(ParsedPacket):
    def __init__(self, type = [0x1A], ID = [0x00,0x01, 0x23, 0x21], capacity=0x03E8, temperature = 0x0045, voltage=0x2034, current = 0, SoC = 0x64, SoH = 0x64):
        self.type = type
        self.ID = ID
        self.capacity = capacity  # in milliampere-hours (mAh)
        self.temperature = temperature # in Celcius 
        self.voltage = voltage    # in volts (V)
        self.current = current.to_bytes(4, byteorder='big', signed=True)  # in milliampare (mA)
        self.SoC = SoC # in %age
        self.SoH = SoH # in %age



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
        if(data.type == 0x00 and data.serial == 0x0000):
            return self._packet_(serial_no = self.ID, type = self.type, request=False)


