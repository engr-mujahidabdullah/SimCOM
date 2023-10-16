import serial
from data_check import CRC16

class Packet:
    def __init__(self):
        pass

    def _packet_(self, Identifier, data):
        if isinstance(data, list):
            size = len(data)
            byte_data = data
        else:
            size = (data.bit_length() + 7) // 8
            data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
            byte_data = [byte for byte in data]
            

        pack  = [Identifier, size] + [byte for byte in byte_data]
        crc_ = CRC16()

        crc = crc_.generate_crc16(pack).to_bytes(2, byteorder='big')
        packet = pack + [byte for byte in crc]
        return packet
