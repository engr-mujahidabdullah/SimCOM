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

class Packet:
    def __init__(self):
        self.crc_ = CRC16()
        pass

    def _packet_(self, serial_no = 0x00000000 , cmd = 00, type = 00, data = 0x00, request = True):
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

        if(type == 0 and req_Header == True):
            pack_len = Header_size + packetLen_size + cmd_size + type_size + crc_size
            pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
            size =  [(size >> 8) & 0xFF, size & 0xFF]
            packet = header + pack_len + cmd + type
        
        else:
            pack_len = Header_size + packetLen_size + cmd_size + type_size + serial_size + payloadLen_size + size + crc_size
            pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
            size =  [(size >> 8) & 0xFF, size & 0xFF]
            packet = header + pack_len + cmd + type + serial_no + size + byte_data
        
        
        crc = self.crc_.min_CRC16(packet).to_bytes(2, byteorder='big')
        print(crc)
        packet = packet + [byte for byte in crc]
        return packet
 