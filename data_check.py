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
    
    def hex_array_to_value(self, hex_values):
        #result = int(''.join(format(x, '02x') for x in hex_values), 16)
        result=int.from_bytes(hex_values, byteorder='big', signed=True)
        return result

    def bit_to_list(self, hex_value, bit_list):
        # Convert the hexadecimal value to a binary string
        binary_string = bin(hex_value)[2:].zfill(16)  # Ensure 16 bits
        print(binary_string)
        # Create a list of variables a1 to a16
        #bit_list = [f'a{i}' for i in range(1, 17)]

        # Create a dictionary where variable names are keys and corresponding bits from the binary string are values
        bit_dict = {bit_list[i]: binary_string[i] for i in range(16)}

        return bit_dict
        # Print the result
    
    def bytes_to_list(self, byte_list, var_list, _bytes_ = 2):
        integer_list = [byte_list[i+1] + (byte_list[i] << 8) for i in range(0, len(byte_list), _bytes_)]
        byte_dict = {var_list[i]: integer_list[i] for i in range(len(var_list))}
        return byte_dict






