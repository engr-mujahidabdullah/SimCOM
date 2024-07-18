CRC16_POLYNOMIAL = 0x1021

class CRC16:
    def __init__(self):
        pass

        """
        Calculate the CRC-16/CCITT-FALSE checksum for the given data.

        Args:
            data (int or list of bytes): The input data to calculate the CRC for.

        Returns:
            int: The calculated CRC16 checksum [2 Bytes].
        """
        
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
    
        """
        Validate the CRC16 checksum of the received packet.

        Args:
            received_packet (list of bytes): The received packet including the CRC field.

        Returns:
            int: 1 if the CRC is valid, 0 otherwise.
        
        """
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

        """
        Convert data to a list of bytes.

        Args:
            data (str, list, or int): The input data to convert.

        Returns:
            list: The converted list of bytes.
        """  
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
    

        """
        Convert a list of hex values to an integer.

        Args:
            hex_values (list of int): The list of hexadecimal values.
            Sign: True/False

        Returns:
            int: The converted integer value.
        """

    def hex_array_to_value(self, hex_values, sign = True):
        #result = int(''.join(format(x, '02x') for x in hex_values), 16)
        result=int.from_bytes(hex_values, byteorder='big', signed=sign)
        return result

        """
        Convert a hexadecimal value to a dictionary of bit values.

        Args:
            hex_value (int): The hexadecimal value to convert.
            bit_list (list of str): The list of variable names for the bits.

        Returns:
            dict: A dictionary mapping variable names to bit values.
        """
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
    

        """
        Convert a list of bytes to a dictionary of integers.

        Args:
            byte_list (list of int): The list of bytes to convert.
            var_list (list of str): The list of variable names for the integers.
            _bytes_ (int): The number of bytes to group together.

        Returns:
            dict: A dictionary mapping variable names to integer values.
        """
    def bytes_to_list(self, byte_list, var_list, _bytes_ = 2):
        integer_list = [byte_list[i+1] + (byte_list[i] << 8) for i in range(0, len(byte_list), _bytes_)]
        byte_dict = {var_list[i]: integer_list[i] for i in range(len(var_list))}
        return byte_dict
    
        """
        Update a hex array with a new value.

        Args:
            updated_value (int): The value to update the array with.
            array_size (int): The size of the hex array.

        Returns:
            list: The updated hex array.
        """
    def update_hex_array(self,  updated_value, array_size):
        hex_array = [0x00] * array_size  # Initialize the hex array with zeros
        
        # Convert the updated value to hexadecimal and update the hex array
        for i in range(array_size):
            shift_amount = 8 * (array_size - 1 - i)  # Calculate the shift amount for each byte
            hex_array[i] = (updated_value >> shift_amount) & 0xFF  # Extract the byte and update the array
        return hex_array

        """
        Convert an integer to a list of bits.

        Args:
            num (int): The integer to convert.
            num_bits (int): The number of bits to extract.

        Returns:
            list: A list of bits representing the integer.
        """
    def int_to_bit_list(self, num, num_bits):
        # Create a mask with the specified number of bits
        mask = (1 << num_bits) - 1
        # Apply the mask to the number to extract the bits
        bits = [int(bool(num & (1 << i))) for i in range(num_bits - 1, -1, -1)]
        return bits
    
        """
        Convert a list of binary digits to a decimal value.

        Args:
            byte_list (list of str): The list of binary digits.

        Returns:
            int: The converted decimal value.
        """
    def binary_to_val(self, byte_list):
        # Convert the binary digits to a binary string
        binary_str = ''.join(byte_list)
        
        # Convert the binary string to an integer
        decimal_num = int(binary_str, 2)
        
        # Convert the decimal number to a hexadecimal byte
        return decimal_num





