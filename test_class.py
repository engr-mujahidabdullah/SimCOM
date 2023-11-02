class parityGenerator:
    def __init__(self, parity_type="even"):
        if parity_type not in ("even", "odd"):
            raise ValueError("Parity type must be 'even' or 'odd'")
        self.parity_type = parity_type

    def generate_parity(self, data, parity_type="even"):
        if parity_type not in ("even", "odd"):
            raise ValueError("Parity type must be 'even' or 'odd")
        parity = 0
        data = [data]
        for byte in data:
            parity ^= byte & 1  # XOR operation with the least significant bit (LSB)
            if parity_type == "odd":
                parity = 1 - parity  # Invert for odd parity
                
        return parity
    
    def data_parity(self, data):
        x  = self.generate_parity(data)
        #data = data[0]
        dat = ((data << 1) | x)
        return dat
    
    def set_parity_type(self, type):
        if type not in ("even", "odd"):
            raise ValueError("Parity type must be 'even' or 'odd")
        else:
            self.parity_type = type

    def break_data(self, data):
        data = [data]
        data = data[0]
        #print(data.bit_length())
        check = (data & 1)
        data = (data >> 1)

        return[check, data]


    def is_valid_parity(self, data, parity_type="even"):
        if parity_type not in ("even", "odd"):
            raise ValueError("Parity type must be 'even' or 'odd")
        
        received_parity = (self.break_data(data)[0])
        # Calculate the expected parity for the given data
        expected_parity = self.generate_parity(self.break_data(data)[1], parity_type)
        print(expected_parity)

        #   # Check if the received parity matches the expected parity
        return received_parity == expected_parity

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