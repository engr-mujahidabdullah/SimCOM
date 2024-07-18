import serial
from data_check import CRC16

req_Header = [0xff, 0x00] #request header
res_Header = [0xff, 0x55] #response header

"""
Data frame structure length
"""
header_size = 2
packetLen_size = 2
cmd_size = 2
type_size = 1
serial_size = 4
payloadLen_size = 2
crc_size = 2

class Packet(CRC16):

    """Initialize the Packet class, which inherits from CRC16."""
    def __init__(self):
        self.parse_packet = ParsedPacket()
        pass

    """
        Create a packet with the given parameters.

        Args:
            serial_no (int or list of bytes): Serial number of the packet.
            cmd (list of bytes): Command bytes.
            type (list of bytes): Type bytes.
            data (list of bytes or str): Data payload.
            request (bool): Whether the packet is a request or response.

        Returns:
            list of bytes: The constructed packet.
    """
    def _packet_(self, serial_no = 0x00000000 , cmd = [0x00,0x00], type = [0x000], data = [], request = True):
        if(data != ''):
            byte_data = self.type_convert(data)
            size = len(byte_data)
        else:
            byte_data = []
            size = 0
            
        serial_no = self.type_convert(serial_no)

        cmd = self.type_convert(cmd)
        type = self.type_convert(type)


        if(request == True):
            header = req_Header
        else:
            header = res_Header


        pack_len = header_size + packetLen_size + cmd_size + type_size + serial_size + payloadLen_size + size + crc_size
        pack_len =  [(pack_len >> 8) & 0xFF, pack_len & 0xFF]
        size =  [(size >> 8) & 0xFF, size & 0xFF]
        if isinstance(type, list):
            pass
        else:
            type = [type]
    
        if isinstance(cmd, list):
            pass
        else:
            cmd = cmd.to_bytes((cmd.bit_length() + 7) // 8,'big')
            cmd = [byte for byte in cmd]

        packet = header + pack_len + type + serial_no + cmd  + size + byte_data
        
        
        crc = self.min_CRC16(packet).to_bytes(2, byteorder='big')
        packet = packet + [byte for byte in crc]
        return packet


class ParsedPacket(Packet):
    def __init__(self):
        """Initialize the ParsedPacket class."""
        self.cmd = 0x0000
        self.type = 0x00
        self.serial = 0x00000000
        self.data_len = 0x0000
        self.data = []
        
    """
        Parse a received packet.

        Args:
            received_packet (list of bytes): The received packet.

        Returns:
            ParsedPacket: The instance of the class with parsed data.
    """

    def parse_received_packet(self, received_packet):
        if self.is_crc_valid(received_packet):
           
            index = 0

            # Skip header
            index += 2

            # Skip packet length
            index += 2

            # Extract type
            self.type = received_packet[index]
            self.type = self.update_hex_array(self.type,1)
            index += 1

            # Extract serial
            self.serial = (received_packet[index] << 24) | (received_packet[index + 1] << 16) | (received_packet[index + 2] << 8) | received_packet[index + 3]
            self.serial = self.update_hex_array(self.serial,4)
            index += 4

            # Extract command
            self.cmd = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract data length
            self.data_len = (received_packet[index] << 8) | received_packet[index + 1]
            index += 2

            # Extract data
            self.data = received_packet[index:-2]

            return self
        else:
            return None

    """
        Get the parsed data from the packet.

        Returns:
            list of bytes or int: The parsed data or -1 if an error occurs.
    """    
    def get_data(self):
        try:
            return self.data
        except:
            return -1

    """
    Print all attributes of the parsed packet instance.
    """       
    def packet_attributes(self):
        attributes = vars(self)  # Get all attributes of the class instance
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

    