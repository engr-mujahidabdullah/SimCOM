from data_check import CRC16

class Battery:
    def __init__(self, type = 0x01, ID = 0x00000001, capacity=0x03E8, temperature = 0x0045, voltage=0x2034, current = 0, SoC = 0x64, SoH = 0x64):
        self.type = type
        self.ID = ID
        self.capacity = capacity  # in milliampere-hours (mAh)
        self.temperature = temperature # in Celcius 
        self.voltage = voltage    # in volts (V)
        self.current = current.to_bytes(4, byteorder='big', signed=True)  # in milliampare (mA)
        self.SoC = SoC # in %age
        self.SoH = SoH # in %age
        self.crc = CRC16()


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

    def rcv_CMD(self, data):

        _from_ = data[0]
        _type_ = data[1]
        _ID_ = data[2:6]
        _CMD_ = data[6:8]
        
        typ = self.type
        id = self.ID.to_bytes(4, 'big')
        _CRC_ = self.crc.check_crc16(data)

        if(_type_ == typ and _ID_ == id and  _CRC_ == True):
            return _CMD_
        else:
            return 0x00FF
        
    def response_rslt(self, data):
        cmd = int.from_bytes(self.rcv_CMD(data), 'big')
        switch_dict = {
            1: self.type,
            3: self.ID,
            5: self.voltage,
            7: self.current,
            3532:self.temperature
        }

        return switch_dict.get(cmd, "Invalid Case")

    

