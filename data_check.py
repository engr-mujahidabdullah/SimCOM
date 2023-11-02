CRC16_POLYNOMIAL = 0x1021

class CRC16:
    def __init__(self):
        pass

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
        
    def type_convert(self, data):
        if isinstance(data, str):
            data = bytes.fromhex(data)
            data = [byte for byte in data]
        if isinstance(data, list):
            pass
        else:
            data_len = (data.bit_length() + 7) // 8
            data = data.to_bytes(data_len, 'big')
            data = [byte for byte in data]
        return data






