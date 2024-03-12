from data_check import CRC16
from Packet import Packet, ParsedPacket

class Battery(ParsedPacket):

    def __init__(self, ID = [0x00,0x00, 0x00, 0x03]):
        self.type = [0x02]
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
        self.charging_curr_max_limt = [0x00, 0x00, 0x00, 0x00]
        self.discharging_curr_max_limt = [0x00, 0x00, 0x00, 0x00]
        self.voltage_high = [0x00, 0x00]
        self.voltage_low = [0x00, 0x00]
        self.cell_voltage_min_limt = [0x00, 0x00]
        self.cell_voltage_max_limt = [0x00, 0x00]
        self.temperature_high = [0x00, 0x00]
        self.temperature_low = [0x00, 0x00]
        self.temperature_min_limt = [0x00, 0x00]
        self.temperature_max_limt = [0x00, 0x00]
        self.all_voltage = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.all_temperature = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.micro_status = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.pack_allVoltage = ["Voltage_" + str(i) for i in range(1, 24)]
        self.pack_allTemperature = ["Temperature_" + str(i) for i in range(1, 5)]
        


    def batt_variable(self):
        # Create a list of variable names and values
        variables = [
            ("Type", self.type),
            ("ID", self.ID),
            ("Capacity", self.capacity),
            ("Temperature", self.temperature),
            ("Voltage", self.voltage),
            ("Current", self.current),
            ("SoC", self.SoC),
            ("SoH", self.SoH),
            ("KWh Charging", self.charging_KWh),
            ("KWh Discharging", self.discharging_KWh),
            ("Charging Time", self.charging_time),
            ("Discgarging Time", self.discharging_time),
            ("Voltage High", self.voltage_high),
            ("Voltage Low", self.voltage_low),
            ("Temperature High", self.temperature_high),
            ("Temperature Low", self.temperature_low),
            ("Cell Voltage max Limt", self.cell_voltage_max_limt),
            ("Cell Voltage min Limt", self.cell_voltage_min_limt),
            ("Temperature max Limt", self.temperature_max_limt),
            ("Temperature min Limt", self.temperature_min_limt),
            ("Charging Curr max Limt", self.charging_curr_max_limt),
            ("Discharging Curr max Limt", self.discharging_curr_max_limt),
            #("All Voltage", self.all_voltage),
            #("All Temperature", self.all_temperature),
            ("Micro Status", self.micro_status),
            ("Status", self.status)
        ]
        return dict(variables)


    def batt_attributes(self):
        attributes = vars(self)  # Get all attributes of the class instance
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

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
 
    def translate_battery_pram(self, var_list, array):
        self.flags = self.bytes_to_list(array, var_list)
        return self.flags
    
    def data_parser(self, cmd, data):
        index = 0

        if(cmd == [0x05, 0x00] or cmd == 0x0500):
            self.all_voltage = data[index: index + 2*23]
            index += 46

            self.current = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.all_temperature = data[index: index + 2*4]
            index += 8

            self.micro_status = data[index: index + 8]
            index += 8

        if(cmd == [0x03, 0x00] or cmd == 0x0300):
            self.cell_voltage_min_limt = [data[index], data[index + 1]]
            index += 2

            self.cell_voltage_max_limt = [data[index], data[index + 1]]
            index += 2

            self.charging_curr_max_limt = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.discharging_curr_max_limt = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.temperature_max_limt = [data[index], data[index + 1]]
            index += 2

            self.temperature_max_limt = [data[index], data[index + 1]]
            index += 2


        if(cmd == [0x01, 0x00] or cmd == 0x0100):
            # Define lists to store the parsed data
            self.voltage = [data[index], data[index + 1]]
            index += 2

            self.voltage_high = [data[index], data[index + 1]]
            index += 2

            self.voltage_low = [data[index], data[index + 1]]
            index += 2

            self.current = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.temperature = [data[index], data[index + 1]]
            index += 2

            self.temperature_high = [data[index], data[index + 1]]
            index += 2

            self.temperature_low = [data[index], data[index + 1]]
            index += 2

            self.SoC = [data[index]]
            index += 1

            self.SoH = [data[index]]
            index += 1

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
            
        else:
            return -1