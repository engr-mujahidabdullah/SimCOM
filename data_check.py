
class CRC16:
    def __init__(self):
        self.crc16_table = [0] * 256
        self._generate_crc16_table()

    def _generate_crc16_table(self):
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0x1021
                else:
                    crc >>= 1
            self.crc16_table[i] = crc

    def generate_crc16(self, data):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
        crc = 0xFFFF
        for byte in data:
            crc = (crc >> 8) ^ self.crc16_table[(crc ^ byte) & 0xFF]
        return crc & 0xFFFF

    def check_crc16(self, data_with_crc):
        crc = 0xFFFF
        data = data_with_crc[:-2]  # Remove the last two bytes (CRC bytes)
        for byte in data:
            crc = (crc >> 8) ^ self.crc16_table[(crc ^ byte) & 0xFF]

        received_crc =  int.from_bytes(data_with_crc[-2:], byteorder='big', signed=False)

        return crc == received_crc
    
    def data_crc(self, data, sign=False):
        checksum = self.generate_crc16(data)
        byte_length = (data.bit_length() + 7) // 8
        print(checksum)
        data_with_crc = data.to_bytes(byte_length, 'big')  + checksum.to_bytes(2, byteorder='big', signed=sign)
        return data_with_crc