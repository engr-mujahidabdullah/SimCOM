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
