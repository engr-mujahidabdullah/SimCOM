import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import serial
import threading  # Import the threading module
from Packet import ParsedPacket

# Create the main application window
app = tk.Tk()
app.title("Serial Communication App")
pack = ParsedPacket()
ser = None  # Initialize the serial object

# Function to handle opening the selected COM port
def open_port():
    global ser
    selected_port = com_port_var.get()
    try:
        ser = serial.Serial(selected_port, 4800)  # Adjust the baud rate if needed
        received_data_text.insert(tk.END, f"Port {selected_port} is opened.\n")
        open_port_button.config(state="disabled")
        close_port_button.config(state="active")
    except Exception as e:
        received_data_text.insert(tk.END, f"Error: {str(e)}\n")

# Function to handle data reception from the selected COM port
def send_data():
    global ser
    selected_port = com_port_var.get()
    pack.serial = serial_number_entry.get()
    pack.type = device_type_entry.get()
    pack.cmd = command_entry.get()
    pack.data = data_entry.get()

    try:
        #ser = serial.Serial(selected_port, 4800)  # Adjust the baud rate if needed
        packet = pack._packet_(pack.serial, pack.cmd, pack.type, pack.data)
        ser.write(packet)
        received_data_text.insert(tk.END, f"data send : {str(packet)}")
    except Exception as e:
        received_data_text.insert(tk.END, f"Error: {str(e)}\n")

# Function to handle closing the selected COM port
def close_port():
    global ser
    if ser is not None and ser.isOpen():
        ser.close()
        received_data_text.insert(tk.END, f"Port {ser.port} is closed.\n")
        open_port_button.config(state="active")
        close_port_button.config(state="disabled")
    else:
        received_data_text.insert(tk.END, "No open port to close.\n")

# Function to continuously read data from the serial port
def read_serial_data():
    selected_port = com_port_var.get()

    try:
        ser = serial.Serial(selected_port, 4800)  # Adjust the baud rate if needed
        while True:
            stream = []
            data = ser.read(2)  # Read one byte at a time
            x = int.from_bytes(data, 'big')
            if data:
                print("data receive")
                if(x == 0xff55):
                    stream.append(data)
                    packet_length = ser.read(2)
                    stream.append(packet_length)
                    leng = int.from_bytes(packet_length, 'big')
                    data = ser.read(leng - 4)
                    stream.append(data)
                stream = [int(byte) for byte_string in stream for byte in byte_string]
                print(stream)
                if pack.is_crc_valid(stream):
                    print("CRC is valid.")
                    _data_ = pack.parse_received_packet(stream)
                    received_data_text.insert(tk.END,f"CMD: 0x{_data_.cmd:04X}\n")
                    received_data_text.insert(tk.END,f"Type: 0x{_data_.type:02X}\n")
                    received_data_text.insert(tk.END,f"Serial: 0x{_data_.serial:08X}\n")
                    received_data_text.insert(tk.END,f"Data Length: {_data_.data_len}\n")
                    print("Data:", end=" ")
                    for i in range(_data_.data_len):
                        print(f"{_data_.data[i]:02X}", end=" ")
                    print()
                app.update()  # Update the GUI to display new data
    except Exception as e:
        print(e)

# Function to populate the COM port dropdown with available ports
def refresh_com_ports():
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = available_ports

# Create and configure widgets
com_port_label = tk.Label(app, text="Select COM Port:")
com_port_label.grid(row=0, column=0, padx=10, pady=10)
com_port_var = tk.StringVar()
com_port_dropdown = ttk.Combobox(app, textvariable=com_port_var)
com_port_dropdown.grid(row=0, column=1, padx=10, pady=10)
refresh_com_ports()  # Initial population of COM ports
com_port_dropdown.set('COM1')  # Set the default COM port

refresh_button = tk.Button(app, text="Refresh COM Ports", command=refresh_com_ports)
refresh_button.grid(row=0, column=2, padx=10, pady=10)

serial_number_label = tk.Label(app, text="Serial Number:")
serial_number_label.grid(row=1, column=0, padx=10, pady=10)
serial_number_entry = tk.Entry(app)
serial_number_entry.grid(row=1, column=1, padx=10, pady=10)

device_type_label = tk.Label(app, text="Device Type:")
device_type_label.grid(row=2, column=0, padx=10, pady=10)
device_type_entry = tk.Entry(app)
device_type_entry.grid(row=2, column=1, padx=10, pady=10)

command_label = tk.Label(app, text="Command:")
command_label.grid(row=3, column=0, padx=10, pady=10)
command_entry = tk.Entry(app)
command_entry.grid(row=3, column=1, padx=10, pady=10)

data_label = tk.Label(app, text="Data:")
data_label.grid(row=4, column=0, padx=10, pady=10)
data_entry = tk.Entry(app)
data_entry.grid(row=4, column=1, padx=10, pady=10)

send_button = tk.Button(app, text="Send Data", command=send_data)
send_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

received_data_text = tk.Text(app, height=10, width=40)
received_data_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Create "Open Port" and "Close Port" buttons
open_port_button = tk.Button(app, text="Open Port", command=open_port)
open_port_button.grid(row=7, column=0, padx=10, pady=10)

close_port_button = tk.Button(app, text="Close Port", command=close_port, state="disabled")
close_port_button.grid(row=7, column=1, padx=10, pady=10)

# Create a separate thread for continuous data reading
data_thread = threading.Thread(target=read_serial_data)
data_thread.daemon = True
data_thread.start()

app.mainloop()
