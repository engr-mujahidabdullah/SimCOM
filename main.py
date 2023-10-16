'''
Includes
'''
import serial
from data_check import CRC16
from Battery import Battery as Batt

# Configure the serial port (adjust the port and baud rate as needed)
ser = serial.Serial('COM4', 4800, parity="E")  
Bat = Batt()

try:
    while True:
        # Read data from the serial port (adjust the number of bytes to read as needed)
        data = ser.read(10)  # Read 10 bytes, adjust this value based on your data size

        # Convert the received bytes to a string
        #data_str = data.decode('utf-8')  # Assuming data is in UTF-8 encoding

        rst = Bat.response_rslt(data)
        ser.write(rst.to_bytes(2, "big"))

        # Process and use the data
        #print(f"Received data: {data_str}")

except KeyboardInterrupt:
    print("Serial reading stopped due to keyboard interrupt.")

finally:
    # Close the serial port when done
    ser.close()
