import serial
from data_check import CRC16

req_Header = [0xff, 0x00]
res_Header = [0xff, 0x55]

Header_size = 2
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

    def _packet_(self, serial_no = 0x00000000 , cmd = [0x00,0x00], type = 0, data = [], request = True):
        if isinstance(data, list):
            size = len(data)
            byte_data = data
        else:
            size = (data.bit_length() + 7) // 8
            data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
            byte_data = [byte for byte in data]
        
        if isinstance(serial_no, list):
            pass
        else:
            Serial_size = (serial_no.bit_length() + 7) // 8
            Serial_data = serial_no.to_bytes(Serial_size, 'big')
            serial_no = [byte for byte in Serial_data]

        if(request == True):
            header = req_Header
        else:
            header = res_Header

        #if(type == 0 and req_Header == True):
        #    pack_len = Header_size + packetLen_size + cmd_size + type_size + crc_size
        #    pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
        #    size =  [(size >> 8) & 0xFF, size & 0xFF]
        #    packet = header + pack_len + cmd + type
        
        #else:

        pack_len = Header_size + packetLen_size + cmd_size + type_size + serial_size + payloadLen_size + size + crc_size
        pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
        size =  [(size >> 8) & 0xFF, size & 0xFF]
        packet = header + pack_len + cmd + type + serial_no + size + byte_data
        
        
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
            result = ParsedPacket()
            index = 0

            # Skip header
            index += 2

            # Skip packet length
            index += 2

            # Extract command
            result.cmd = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract type
            result.type = received_packet[index]
            index += 1

            # Extract serial
            result.serial = (received_packet[index] << 24) | (received_packet[index + 1] << 16) | (received_packet[index + 2] << 8) | received_packet[index + 3]
            index += 4

            # Extract data length
            result.data_len = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract data
            result.data = received_packet[index:-2]

            return result

    