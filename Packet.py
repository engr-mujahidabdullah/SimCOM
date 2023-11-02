import serial
from data_check import CRC16

req_Header = [0xff, 0x00]
res_Header = [0xff, 0x55]

header_size = 2
packetLen_size = 2
cmd_size = 2
type_size = 1
serial_size = 4
payloadLen_size = 2
crc_size = 2

class Packet(CRC16):
    def __init__(self):
        #self.crc = CRC16()
        self.parse_packet = ParsedPacket()
        pass

    def _packet_(self, serial_no = 0x00000000 , cmd = [0x00,0x00], type = [0x000], data = [], request = True):
        if(data != ''):
            byte_data = self.type_convert(data)
            size = len(byte_data)
        else:
            byte_data = []
            size = 0
            
        serial_no = self.type_convert(serial_no)

        cmd = self.type_convert(cmd)
        type = self.type_convert(type)


        if(request == True):
            header = req_Header
        else:
            header = res_Header


        pack_len = header_size + packetLen_size + cmd_size + type_size + serial_size + payloadLen_size + size + crc_size
        pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
        size =  [(size >> 8) & 0xFF, size & 0xFF]
        if isinstance(type, list):
            pass
        else:
            type = [type]
    
        if isinstance(cmd, list):
            pass
        else:
            cmd = cmd.to_bytes((cmd.bit_length() + 7) // 8,'big')
            cmd = [byte for byte in cmd]

        packet = header + pack_len + type + serial_no + cmd  + size + byte_data
        
        
        crc = self.min_CRC16(packet).to_bytes(2, byteorder='big')
        packet = packet + [byte for byte in crc]
        return packet
 
class ParsedPacket(Packet):
    def __init__(self):
        self.cmd = 0x0000
        self.type = 0x00
        self.serial = 0x00000000
        self.data_len = 0x0000
        self.data = []
        

    def parse_received_packet(self, received_packet):
        if self.is_crc_valid(received_packet):
           
            index = 0

            # Skip header
            index += 2

            # Skip packet length
            index += 2

            # Extract type
            self.type = received_packet[index]
            index += 1

            # Extract serial
            self.serial = (received_packet[index] << 24) | (received_packet[index + 1] << 16) | (received_packet[index + 2] << 8) | received_packet[index + 3]
            index += 4

            # Extract command
            self.cmd = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract data length
            self.data_len = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract data
            self.data = received_packet[index:-2]

            return self
        
    def get_data(self):
        try:
            return self.data
        except:
            return -1
        
    def packet_attributes(self):
        attributes = vars(self)  # Get all attributes of the class instance
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

    