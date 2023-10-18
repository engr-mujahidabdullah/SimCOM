from data_check import CRC16
import serial


from Packet import Packet
pack = Packet()

packet_to_send = pack._packet_([0x00, 0xAA, 0xAB, 0x01], [0x12, 0x34], [0x01], [0x12, 0x34, 0x56])

# Configure the serial port (adjust the port and baud rate as needed)
ser = serial.Serial('COM5', 4800)  # Replace 'COM1' with the correct serial port name

# Define the byte array to send
print(packet_to_send)

try:
    # Send the byte array to the serial port
    ser.write(packet_to_send)
    print("Byte array sent to serial port.")

    
except serial.SerialException as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial port when done
    ser.close()
