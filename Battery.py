class Battery:
    def __init__(self, type = 0x01, ID = 0x0001, capacity=0x03E8, temperature = 0x0045, voltage=3.7, current = 0.0, SoC = 0x64, SoH = 0x64):
        self.type = type
        self.ID = ID
        self.capacity = capacity  # in milliampere-hours (mAh)
        self.temperature = temperature # in Celcius 
        self.voltage = voltage    # in volts (V)
        self.current = current  # in milliampare (mA)
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

