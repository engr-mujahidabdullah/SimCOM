import serial

# Configure the serial port (adjust the port and baud rate as needed)
ser = serial.Serial('COM5', 4800)  # Replace 'COM1' with the correct serial port name

header = [0x00, 0x00]
stream = []

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
            print(stream)
            stream = [int(byte) for byte_string in stream for byte in byte_string]
            print(stream)
except KeyboardInterrupt:
    print("Serial data capture stopped due to keyboard interrupt.")
except serial.SerialException as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial port when done
    ser.close()
