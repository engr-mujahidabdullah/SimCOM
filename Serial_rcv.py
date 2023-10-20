import serial
from Packet import ParsedPacket
from data_check import CRC16

# Configure the serial port (adjust the port and baud rate as needed)
ser = serial.Serial('COM14', 4800)  # Replace 'COM1' with the correct serial port name

header = [0x00, 0x00]
stream = []
crc = CRC16()
packet = ParsedPacket()

try:
    while True:
        stream = []
        data = ser.read(2)  # Read one byte at a time
        x = int.from_bytes(data, 'big')
        if data:
            if(x == 0xff00):
                stream.append(data)
                packet_length = ser.read(2)
                stream.append(packet_length)
                leng = int.from_bytes(packet_length, 'big')
                data = ser.read(leng - 4)
                stream.append(data)
            stream = [int(byte) for byte_string in stream for byte in byte_string]
            print(stream)
            if crc.is_crc_valid(stream):
                print("CRC is valid.")
                _data_ = packet.parse_received_packet(stream)
                print(f"CMD: 0x{_data_.cmd:04X}")
                print(f"Type: 0x{_data_.type:02X}")
                print(f"Serial: 0x{_data_.serial:08X}")
                print(f"Data Length: {_data_.data_len}")
                print("Data:", end=" ")
                for i in range(_data_.data_len):
                    print(f"{_data_.data[i]:02X}", end=" ")
                print()


except KeyboardInterrupt:
    print("Serial data capture stopped due to keyboard interrupt.")
except serial.SerialException as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial port when done
    ser.close()
