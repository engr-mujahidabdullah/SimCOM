CRC16_POLYNOMIAL = 0x1021

class CRC16:
    def __init__(self):
        self.crc16_table = [0] * 256
        #self._generate_crc16_table()

    def _generate_crc16_table(self):
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ CRC16_POLYNOMIAL

                else:
                    crc >>= 1
            self.crc16_table[i] = crc


    def generate_crc16(self, data):
        if isinstance(data, list):
            pass
        else:
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

        received_crc =  int.from_bytes(data_with_crc[-2:], byteorder='big', signed=True)
        return crc == received_crc

    def data_crc(self, data, sign=False):
        checksum = self.generate_crc16(data)
        byte_length = (data.bit_length() + 7) // 8
        print(checksum)
        data_with_crc = data.to_bytes(byte_length, 'big')  + checksum.to_bytes(2, byteorder='big', signed=sign)
        return data_with_crc
    
    def min_CRC16(self, data):
        if isinstance(data, list):
            pass
        else:
            data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
        crc = 0xFFFF
        poly = CRC16_POLYNOMIAL

        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc = crc << 1

        return  crc & 0xFFFF  # Ensure the result is a 16-bit value
    
    def is_crc_valid(self, received_packet):
        # Calculate the CRC for the received packet (excluding the CRC field)
        calculated_crc = self.min_CRC16(received_packet[:-2])

    # Extract the received CRC from the packet
        received_crc = (received_packet[-2] << 8) | received_packet[-1]

    # Compare the calculated CRC with the received CRC
        if calculated_crc == received_crc:
            return 1  # Valid CRC
        else:
            return 0  # Invalid CRC






