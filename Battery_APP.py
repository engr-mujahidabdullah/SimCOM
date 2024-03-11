import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import serial
import threading
from Packet import ParsedPacket
from Battery import Battery
import serial.tools.list_ports
import asyncio
import csv

def open_port():
    global ser, reading_data
    selected_port = com_port_var.get()
    try:
        ser = serial.Serial(selected_port, 4800, parity=serial.PARITY_EVEN)  # Adjust the baud rate if needed
        received_data_text.insert(tk.END, f"Port {selected_port} is opened.\n")
        open_port_button.config(state=tk.DISABLED)
        close_port_button.config(state=tk.NORMAL)
        reading_data = True  # Start reading data
        data_thread = threading.Thread(target=read_serial_data)
        data_thread.daemon = True
        data_thread.start()
    except Exception as e:
        received_data_text.insert(tk.END, f"Error: {str(e)}\n")

def close_port():
    global ser, reading_data
    if ser is not None and ser.is_open:
        ser.close()
        received_data_text.insert(tk.END, f"Port {ser.port} is closed.\n")
        open_port_button.config(state=tk.NORMAL)
        close_port_button.config(state=tk.DISABLED)
        reading_data = False  # Stop reading data
    else:
        received_data_text.insert(tk.END, "No open port to close.\n")

def read_serial_data():
    global flag_dict, selected_port
    selected_port = com_port_var.get()

    try:
        while True:
            stream = []
            data = ser.read(2)  # Read one byte at a time
            x = int.from_bytes(data, 'big')
            if data:
                if x == 0xff00 or x == 0xff55:
                    stream.append(data)
                    packet_length = ser.read(2)
                    print(packet_length)
                    stream.append(packet_length)
                    leng = int.from_bytes(packet_length, 'big')
                    d_size = leng - 4
                    print(d_size)
                    data = ser.read(d_size)
                    stream.append(data)
                ser.reset_input_buffer()
                stream = [int(byte) for byte_string in stream for byte in byte_string]
                print(stream)


                if pack.is_crc_valid(stream):
                    print("CRC is valid.")
                    _data_ = pack.parse_received_packet(stream)
                    received_data_text.insert(tk.END, f"CMD: {hex(_data_.cmd)}\n")
                    received_data_text.insert(tk.END, f"Type: {hex(_data_.type)}\n")
                    received_data_text.insert(tk.END, f"Serial: {hex(_data_.serial)}\n")
                    received_data_text.insert(tk.END, f"Data Length: {_data_.data_len}\n")
                    received_data_text.insert(tk.END, f"Data: {_data_.data}\n")
                    c.type = c.type_convert(_data_.type)
                    c.ID = c.type_convert(_data_.serial)
                    c.data_parser(_data_.cmd, _data_.data)
                    Voltage_data_text.insert(tk.END, f"{[c.all_voltage[i+1] + (c.all_voltage[i] << 8) for i in range(0, len(c.all_voltage), 2)]}\n")
                    Voltage_data_text.see(tk.END)
                    received_data_text.see(tk.END)

                    #c.translate_Charger_status(c.status, c.char0200)
                    update_variable_values()
                else:
                    print("Invalid CRC")
                app.update()
    except Exception as e:
        print(e)
        if ser is not None and ser.is_open:
            close_port()
            print ('Reset exception')
            open_port()
        pass

def send_data():    
    global ser, selected_port 
    selected_port = com_port_var.get()
    pack.serial = serial_number_var.get()
    pack.type = device_type_var.get()
    pack.cmd = command_var.get()
    pack.data = data_var.get()
    ser.reset_input_buffer()

    try:
        packet = pack._packet_(pack.serial, pack.cmd, pack.type, pack.data)
        ser.write(packet)
        received_data_text.insert(tk.END, f"data send : {str(packet)} \n")
    except Exception as e:
        received_data_text.insert(tk.END, f"Error: {str(e)}\n")

def refresh_com_ports():
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = available_ports
    com_port_var.set(available_ports[0])  # Set the default COM port

def update_variable_values():
 
    for var_name, var_value in c.batt_variable().items():
        variables_values[var_name].configure(state="normal")
        variables_values[var_name].delete("1.0", tk.END)  # Clear the existing text
        variables_values[var_name].insert(tk.END, c.hex_array_to_value(var_value))  # Set the new value
        variables_values[var_name].configure(state="disabled")


    for var_name, var_value in c.translate_battery_pram(c.pack_allVoltage, c.all_voltage).items():
        Vol_values[var_name].configure(state="normal")
        Vol_values[var_name].delete("1.0", tk.END)  # Clear the existing text
        Vol_values[var_name].insert(tk.END, var_value)  # Set the new value
        Vol_values[var_name].configure(state="disabled")

    for var_name, var_value in c.translate_battery_pram(c.pack_allTemperature, c.all_temperature).items():
        Tem_values[var_name].configure(state="normal")
        Tem_values[var_name].delete("1.0", tk.END)  # Clear the existing text
        Tem_values[var_name].insert(tk.END, var_value * 0.01)  # Set the new value
        Tem_values[var_name].configure(state="disabled")

import time
def auto_send():
    while(checkbox_var.get() == True):
        send_data()
        time.sleep(autoTime_var.get())


def auto_sender():
    if(checkbox_var.get() == True):
        send_thread = threading.Thread(target=auto_send)
        send_thread.daemon = True
        send_thread.start()
    else:
        send_data()


app = tk.Tk()
app.title("Battery Communication App")
c = Battery()
pack = ParsedPacket()
ser = None
reading_data = False
variables_dict = c.batt_variable()




# Create and configure the tkinter widgets
com_port_label = tk.Label(app, text="Select COM Port:")
com_port_var = tk.StringVar()
com_port_dropdown = ttk.Combobox(app, textvariable=com_port_var)
refresh_com_ports()  # Initial population of COM ports
refresh_button = tk.Button(app, text="Refresh COM", command=refresh_com_ports)
open_port_button = tk.Button(app, text="Open Port", command=open_port)
close_port_button = tk.Button(app, text="Close Port", command=close_port, state=tk.DISABLED)
serial_number_label = tk.Label(app, text="Serial Number:")
serial_number_var = tk.StringVar()
serial_number_var.set("00000001")
serial_number_entry = tk.Entry(app, textvariable=serial_number_var)
device_type_label = tk.Label(app, text="Device Type:")
device_type_var = tk.StringVar()
device_type_var.set("01")
device_type_entry = tk.Entry(app, textvariable=device_type_var)
command_label = tk.Label(app, text="Command:")
command_var = tk.StringVar()
command_entry = tk.Entry(app, textvariable=command_var)
command_var.set("0000")
data_label = tk.Label(app, text="Data:")
data_var = tk.StringVar()
data_entry = tk.Entry(app, textvariable=data_var)
send_button = tk.Button(app, text="Send Data", command=auto_sender)
received_data_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=120, height=10)
autoTime_label = tk.Label(app, text="Auto Time (sec)")
autoTime_var = tk.IntVar()
autoTime_entry = tk.Entry(app, textvariable=autoTime_var)
autoTime_var.set(1)
checkbox_var = tk.BooleanVar()
checkbox = ttk.Checkbutton(app, text="Auto-Send", variable=checkbox_var)
Voltage_data_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=120, height=10)


# Place widgets in the window
com_port_label.grid(row=0, column=0)
com_port_dropdown.grid(row=0, column=1)
refresh_button.grid(row=0, column=2)
open_port_button.grid(row=0, column=3)
close_port_button.grid(row=0, column=4)
serial_number_label.grid(row=1, column=0)
serial_number_entry.grid(row=1, column=1)
device_type_label.grid(row=2, column=0)
device_type_entry.grid(row=2, column=1)
command_label.grid(row=3, column=0)
command_entry.grid(row=3, column=1)
data_label.grid(row=4, column=0)
data_entry.grid(row=4, column=1)
autoTime_label.grid(row=5, column=0)
autoTime_entry.grid(row=5, column=1)
checkbox.grid(row=6, column=0)
send_button.grid(row=6, column=1)
received_data_text.grid(row=25, column=0, columnspan=12, rowspan=10)
Voltage_data_text.grid(row=35, column=0, columnspan=12, rowspan=10)

row = 1

variables_labels = {}
variables_values = {}

for var_name, var_value in variables_dict.items():
    label = tk.Label(app, text=f"{var_name}:")
    label.grid(row=row, column=2)
    
    value_text = tk.Text(app, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, c.hex_array_to_value(var_value))
    value_text.configure(state="disabled")
    value_text.grid(row=row, column=3)

    variables_labels[var_name] = label
    variables_values[var_name] = value_text
    row += 1

Tem_labels = {}
Tem_values = {}


for var_name, var_value in c.translate_battery_pram(c.pack_allTemperature, c.all_temperature).items():
    label = tk.Label(app, text=f"{var_name}:")
    label.grid(row=row, column=2)
    
    value_text = tk.Text(app, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, var_value)
    value_text.configure(state="disabled")
    value_text.grid(row=row, column=3)

    Tem_labels[var_name] = label
    Tem_values[var_name] = value_text
    row += 1


row = 1

Vol_labels = {}
Vol_values = {}


for var_name, var_value in c.translate_battery_pram(c.pack_allVoltage, c.all_voltage).items():
    label = tk.Label(app, text=f"{var_name}:")
    label.grid(row=row, column=4)
    
    value_text = tk.Text(app, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, var_value)
    value_text.configure(state="disabled")
    value_text.grid(row=row, column=5)

    Vol_labels[var_name] = label
    Vol_values[var_name] = value_text
    row += 1


# Rest of your code
app.mainloop()      