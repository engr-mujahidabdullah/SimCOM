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
        self.macro_status = [0x00, 0x00, 0x00, 0x00]
        self.session_id = [0x00, 0x00]
        self.bat_en = [0x00]
        self.adc_vals = [0x00] * 56
        self.eeprom_start = [0x00, 0x00]
        self.eeprom_tostart = [0x00, 0x00]
        self.eeprom_end = [0x00, 0x00]
        self.pack_allVoltage = ["Voltage_" + str(i) for i in range(1, 24)]
        self.pack_allTemperature = ["Temperature_" + str(i) for i in range(1, 5)]
        status_flags = ["BAT_en/dn", "Char_SW_Stat", "Dis_SW_Stat", "Char_SW_Fault", "Dis_SW_Fault", "Over_Temp_flag", "Un_Temp_flag",
                       "Char_OC", "Dis_OC", "Temper_SW_flag", "BAT_UV", "BAT_OV", "New_CONFIG_flag", "Ext_EEPROM_full", "TBD1", "TBD2", "TBD3", "Vol_Limt_mismatch"]
        self.status_ = status_flags + ["UV_Cell" + str(i) for i in range(1, 24)] + ["OV_Cell" + str(i) for i in range(1, 24)]
        self.adc = ["Voltage_ADC_Cell_" + str(i) for i in range(1, 24)] + ["Current_ADC"] + ["Temperature_ADC_" + str(i) for i in range(1, 5)]
        self.eeprom_data = [0x00] * 128

        eep_page_data = ["Data Index 1", "Data Index 2","-","-","Years","Months","Days1","Days2","Hours","Minutes","Seconds"]
        eep_page_data = eep_page_data + [f"cell_{i}" for i in range(1, 24) for _ in range(2)] 
        eep_page_data = eep_page_data + ["Peak Charging Current", "Peak Charging Current","Peak Charging Current","Peak Charging Current","Average Charging Current",
                                         "Average Charging Current","Average Charging Current","Average Charging Current","Peak Discharging Current","Peak Discharging Current",
                                         "Peak Discharging Current","Peak Discharging Current","Average Discharging Current","Average Discharging Current","Average Discharging Current",
                                         "Average Discharging Current","Max Temperature 1","Max Temperature 1","Max Temperature 2","Max Temperature 2","Max Temperature 3","Max Temperature 3",
                                         "Max Temperature 4","Max Temperature 4","Micro Status Flag","Micro Status Flag","Micro Status Flag","Micro Status Flag","Micro Status Flag","Micro Status Flag",
                                         "Micro Status Flag","Micro Status Flag","SOC","SOH","Discharging Wh","Discharging Wh","Discharging Wh","Discharging Wh","Charging Wh","Charging Wh","Charging Wh",
                                         "Charging Wh","Discharging Timer","Discharging Timer","Discharging Timer","Discharging Timer","Charging Timer","Charging Timer","Charging Timer","Charging Timer" ]
        self.eeprom_page_data = eep_page_data + ["TBD_" + str(i) for i in range(1, 22)]

        self.variables_to = ["type","ID","capacity","temperature","voltage","current", "SoC", 
                          "SoH","charging_KWh","discharging_KWh","charging_time","discharging_time", 
                          "voltage_high","voltage_low","temperature_high","temperature_low","cell_voltage_max_limt", 
                          "cell_voltage_min_limt","temperature_max_limt","temperature_min_limt","charging_curr_max_limt", 
                          "discharging_curr_max_limt"]

        



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
            ("Discharging Curr max Limt", self.discharging_curr_max_limt)
            #("All Voltage", self.all_voltage),
            #("All Temperature", self.all_temperature),
            #("Micro Status", self.micro_status)
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
    
    def translate_eeprom_page(self, var_list, array):
        page = tuple(zip(var_list, array))
        print(page)
        return page
    
    def translate_Battery_status(self, state, array):
        state = state[::-1]
        status_dict = {}
        bit_list = [bit for byte in array for bit in bin(byte)[2:].zfill(8)]
        #bit_list = bit_list[::-1]
        if len(state) == len(bit_list):
            for i in range(len(state)):
                status_dict[state[i]] = bit_list[i]
        else:
            print("Error: State and bit_list must have the same length.")

        return status_dict
    
    def send_payload(self, cmd):
        data =  []
        if(cmd == [0x02, 0x00] or cmd == "0200"):
            data = self.session_id + self.macro_status + self.bat_en
        
        if(cmd == [0x04, 0x00] or cmd == "0400"):
            data = self.cell_voltage_min_limt + self.cell_voltage_max_limt + self.charging_curr_max_limt + self.discharging_curr_max_limt + self.temperature_max_limt + self.temperature_min_limt

        if(cmd == [0x06, 0x00] or cmd == "0600"):
            data = self.micro_status
    
        if(cmd == [0x07, 0x00] or cmd == "0700"):
            data = self.adc_vals

        if(cmd == [0x0C, 0x00] or cmd == "0C00"):
            data = self.eeprom_tostart

        return data
    
    def set_variable(self, var_name, value):
            if hasattr(self, var_name):
                setattr(self, var_name, value)
            else:
                print(f"Error: '{var_name}' is not a valid variable in this class.")

    
    def data_parser(self, cmd, data):
        index = 0

        if(cmd == [0x0B, 0x00] or cmd == 0x0B00 or cmd == [0x0C, 0x00] or cmd == 0x0C00):
            self.eeprom_data = data[index: index + 128]
            print(self.eeprom_data)
            index += 128

        if(cmd == [0x0D, 0x00] or cmd == 0x0D00):
            self.eeprom_start = [data[index], data[index + 1]]
            index += 2

            self.eeprom_end = [data[index], data[index + 1]]
            index += 2

        if(cmd == [0x07, 0x00] or cmd == 0x0700):
            self.adc_vals = data[index: index + 2*28]
            index += 56

        if(cmd == [0x06, 0x00] or cmd == 0x0600):
            self.micro_status = data[index: index + 8]
            index += 8

        if(cmd == [0x05, 0x00] or cmd == 0x0500):
            self.all_voltage = data[index: index + 2*23]
            index += 46

            self.current = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.all_temperature = data[index: index + 2*4]
            index += 8

            self.micro_status = data[index: index + 8]
            index += 8

        if(cmd == [0x03, 0x00] or cmd == [0x04, 0x00] or cmd == 0x0400 or cmd == 0x0300):
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

            self.temperature_min_limt = [data[index], data[index + 1]]
            index += 2

        if(cmd == [0x02, 0x00] or cmd == 0x0200):
            self.session_id = [data[index], data[index + 1]]
            index += 2

            self.macro_status = [data[index], data[index + 1], data[index + 2], data[index + 3]]
            index += 4

            self.bat_en = data[index]
            index += 1
    
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
        
    def eprom_data_prompt(self, data):
        vars = [
            ("Data Index", data[0:2]),
            ("-", data[2:4]),
            ("Years", hex(data[4])),
            ("Months", hex(data[5])),
            ("Date", hex(data[6])),
            ("Day", hex(data[7])),
            ("Hours",hex(data[8])),
            ("Minute",hex(data[9])),
            ("Second",hex(data[10])),
            ("Cell 1",self.hex_array_to_value(data[11:13])),
            ("Cell 2",self.hex_array_to_value(data[13:15])),
            ("Cell 3",self.hex_array_to_value(data[15:17])),
            ("Cell 4",self.hex_array_to_value(data[17:19])),
            ("Cell 5",self.hex_array_to_value(data[19:21])),
            ("Cell 6",self.hex_array_to_value(data[21:23])),
            ("Cell 7",self.hex_array_to_value(data[23:25])),
            ("Cell 8",self.hex_array_to_value(data[25:27])),
            ("Cell 9",self.hex_array_to_value(data[27:29])),
            ("Cell 10",self.hex_array_to_value(data[29:31])),
            ("Cell 11",self.hex_array_to_value(data[31:33])),
            ("Cell 12",self.hex_array_to_value(data[33:35])),
            ("Cell 13",self.hex_array_to_value(data[35:37])),
            ("Cell 14",self.hex_array_to_value(data[37:39])),
            ("Cell 15",self.hex_array_to_value(data[39:41])),
            ("Cell 16",self.hex_array_to_value(data[41:43])),
            ("Cell 17",self.hex_array_to_value(data[43:45])),
            ("Cell 18",self.hex_array_to_value(data[45:47])),
            ("Cell 19",self.hex_array_to_value(data[47:49])),
            ("Cell 20",self.hex_array_to_value(data[49:51])),
            ("Cell 21",self.hex_array_to_value(data[51:53])),
            ("Cell 22",self.hex_array_to_value(data[53:55])),
            ("Cell 23",self.hex_array_to_value(data[55:57])),
            ("Peak Charging Current",self.hex_array_to_value(data[57:61])),
            ("Average Charging Current",self.hex_array_to_value(data[61:65])),
            ("Peak Discharging Current",self.hex_array_to_value(data[65:69])),
            ("Average Discharging Current",self.hex_array_to_value(data[69:73])),
            ("Max Temperature 1",self.hex_array_to_value(data[73:75])),
            ("Max Temperature 2",self.hex_array_to_value(data[75:77])),
            ("Max Temperature 3",self.hex_array_to_value(data[77:79])),
            ("Max Temperature 4",self.hex_array_to_value(data[79:81])),
            ("Micro Status Flag",self.hex_array_to_value(data[81:89])),
            ("SoC", data[89]),
            ("SoH", data[90]),
            ("Discharging Wh",self.hex_array_to_value(data[91:95])),
            ("Charging Wh",self.hex_array_to_value(data[95:99])),
            ("Discharging Timer",self.hex_array_to_value(data[99:103])),
            ("Charging Timer",self.hex_array_to_value(data[103:107])),
            ("TBD",self.hex_array_to_value(data[107:]))
        ]
        return vars
        