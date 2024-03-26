import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import serial
import threading
from Packet import ParsedPacket
from Battery import Battery
import serial.tools.list_ports


root = tk.Tk() 
root.title("Tab Widget") 
tabControl = ttk.Notebook(root) 

tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Main') 
tabControl.add(tab2, text ='Flags/ADC')
tabControl.add(tab4, text ='EEPROM') 
tabControl.add(tab3, text ='Voltage') 
tabControl.pack(expand = 1, fill ="both") 


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
                tab1.update()
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

    c.session_id = Session_ID_var.get()
    c.macro_status = Reset_macro_var.get()
    c.bat_en = bat_en_var.get()
    c.eeprom_start = eeprom_start_var.get()
    c.eeprom_end = eeprom_end_var.get()
    c.eeprom_tostart = eeprom_tostart_var.get()

    for var_name, var_value in c.batt_variable().items():
        var_value_int = variables_values[var_name].get("1.0", tk.END).strip()
        var_value = c.update_hex_array(int(var_value_int), len(var_value))

    adc_list = []
    for var_name, var_value in c.translate_battery_pram(c.adc, c.adc_vals).items():
        adc_value_int = adc_values[var_name].get("1.0", tk.END).strip()
        adc_list = adc_list + (c.update_hex_array(int(adc_value_int), 2))
    c.adc_vals = adc_list
    
    status_value_list = []
    for var_name, var_value in c.translate_Battery_status(c.status_, c.micro_status).items():
        status_value_list.append(status_values[var_name].get().strip())
    c.micro_status = c.update_hex_array(int(c.binary_to_val(status_value_list)), len(c.micro_status))
    print(c.micro_status)

    pack.data = c.send_payload(pack.cmd)
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
        variables_values[var_name].configure(state="normal")


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

    for var_name, var_value in c.translate_battery_pram(c.adc, c.adc_vals).items():
        adc_values[var_name].configure(state="normal")
        adc_values[var_name].delete("1.0", tk.END)  # Clear the existing text
        adc_values[var_name].insert(tk.END, var_value)  # Set the new value
        adc_values[var_name].configure(state="normal")

    for vars in c.translate_eeprom_page(c.eeprom_page_data, c.eeprom_data):
        eeprom_values[vars[0]].configure(state="normal")
        eeprom_values[vars[0]].delete("1.0", tk.END)  # Clear the existing text
        eeprom_values[vars[0]].insert(tk.END, vars[1])  # Set the new value
        eeprom_values[vars[0]].configure(state="normal")

    for var_name, var_value in c.translate_Battery_status(c.status_, c.micro_status).items():
        status_values[var_name].configure(state="normal")
        status_values[var_name].delete(0, tk.END)  # Clear the existing text
        status_values[var_name].insert(tk.END, var_value)  # Set the new value
        status_values[var_name].configure(state="normal")


    eeprom_start_entry.configure(state="normal")
    eeprom_start_entry.delete(0, tk.END)
    eeprom_start_entry.insert(tk.END, c.eeprom_start)
    eeprom_start_entry.configure(state="normal")

    eeprom_tostart_entry.configure(state="normal")
    eeprom_tostart_entry.delete(0, tk.END)
    eeprom_tostart_entry.insert(tk.END, c.eeprom_tostart)
    eeprom_tostart_entry.configure(state="normal")

    eeprom_end_entry.configure(state="normal")
    eeprom_end_entry.delete(0, tk.END)
    eeprom_end_entry.insert(tk.END, c.eeprom_end)
    eeprom_end_entry.configure(state="normal")

    Reset_macro_entry.configure(state="normal")
    Reset_macro_entry.delete(0, tk.END)
    Reset_macro_entry.insert(tk.END, c.macro_status)
    Reset_macro_entry.configure(state="normal")

    bat_en_entry.configure(state="normal")
    bat_en_entry.delete(0, tk.END)
    bat_en_entry.insert(tk.END, c.bat_en)
    bat_en_entry.configure(state="normal")


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


#app = tk.Tk()
#app.title("Battery Communication App")
c = Battery()
pack = ParsedPacket()
ser = None
reading_data = False
variables_dict = c.batt_variable()




# Create and configure the tkinter widgets
com_port_label = tk.Label(tab1, text="Select COM Port:")
com_port_var = tk.StringVar()
com_port_dropdown = ttk.Combobox(tab1, textvariable=com_port_var)
refresh_com_ports()  # Initial population of COM ports
refresh_button = tk.Button(tab1, text="Refresh COM", command=refresh_com_ports)
open_port_button = tk.Button(tab1, text="Open Port", command=open_port)
close_port_button = tk.Button(tab1, text="Close Port", command=close_port, state=tk.DISABLED)
serial_number_label = tk.Label(tab1, text="Serial Number:")
serial_number_var = tk.StringVar()
serial_number_var.set("00000001")
serial_number_entry = tk.Entry(tab1, textvariable=serial_number_var)
device_type_label = tk.Label(tab1, text="Device Type:")
device_type_var = tk.StringVar()
device_type_var.set("01")
device_type_entry = tk.Entry(tab1, textvariable=device_type_var)
command_label = tk.Label(tab1, text="Command:")
command_var = tk.StringVar()
command_combo = ttk.Combobox(tab1, textvariable=command_var)
command_combo['values'] = ("0100", "0200", '0300', '0400', '0500', '0600', '0700', '0B00', '0C00', '0D00')
data_label = tk.Label(tab1, text="Data:")
data_var = tk.StringVar()
data_entry = tk.Entry(tab1, textvariable=data_var)
send_button = tk.Button(tab1, text="Send Data", command=auto_sender)
received_data_text = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, width=120, height=10)
autoTime_label = tk.Label(tab1, text="Auto Time (sec)")
autoTime_var = tk.IntVar()
autoTime_entry = tk.Entry(tab1, textvariable=autoTime_var)
autoTime_var.set(1)
checkbox_var = tk.BooleanVar()
checkbox = ttk.Checkbutton(tab1, text="Auto-Send", variable=checkbox_var)
Session_ID_label = tk.Label(tab1, text="Session ID:")
Session_ID_var = tk.StringVar()
Session_ID_var.set("0001")
Session_ID_entry = tk.Entry(tab1, textvariable=Session_ID_var)
Reset_macro_label = tk.Label(tab1, text="Reset Macro Status Bits:")
Reset_macro_var = tk.StringVar()
Reset_macro_var.set("00000001")
Reset_macro_entry = tk.Entry(tab1, textvariable=Reset_macro_var)
bat_en_label = tk.Label(tab1, text="Battery EN/DS Status:")
bat_en_var = tk.StringVar()
bat_en_var.set("01")
bat_en_entry = tk.Entry(tab1, textvariable=bat_en_var)
Voltage_data_text = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, width=120, height=10)

eeprom_start_label = tk.Label(tab4, text="EEPROM Start Addr:")
eeprom_start_var = tk.StringVar()
eeprom_start_entry = tk.Entry(tab4, textvariable=eeprom_start_var)

eeprom_end_label = tk.Label(tab4, text="EEPROM End Addr:")
eeprom_end_var = tk.StringVar()
eeprom_end_entry = tk.Entry(tab4, textvariable=eeprom_end_var)

eeprom_tostart_label = tk.Label(tab4, text="EEPROM Start Addr to read:")
eeprom_tostart_var = tk.StringVar()
eeprom_tostart_entry = tk.Entry(tab4, textvariable=eeprom_tostart_var)

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
command_combo.grid(row=3, column=1)
data_label.grid(row=4, column=0)
data_entry.grid(row=4, column=1)
autoTime_label.grid(row=5, column=0)
autoTime_entry.grid(row=5, column=1)
checkbox.grid(row=6, column=0)
send_button.grid(row=6, column=1)
Session_ID_label.grid(row = 7, column =0)
Session_ID_entry.grid(row = 7, column =1)
Reset_macro_label.grid(row = 8, column =0)
Reset_macro_entry.grid(row = 8, column =1)
bat_en_label.grid(row = 9, column =0)
bat_en_entry.grid(row = 9, column =1)
received_data_text.grid(row=25, column=0, columnspan=12, rowspan=10)
Voltage_data_text.grid(row=1, column=0, columnspan=12, rowspan=10)
eeprom_start_label.grid(row=0, column=0)
eeprom_start_entry.grid(row=0, column=1)
eeprom_end_label.grid(row=1, column=0)
eeprom_end_entry.grid(row=1, column=1)
eeprom_tostart_label.grid(row=0, column=2)
eeprom_tostart_entry.grid(row=0, column=3)

row = 1

variables_labels = {}
variables_values = {}

for var_name, var_value in variables_dict.items():
    label = tk.Label(tab1, text=f"{var_name}:")
    label.grid(row=row, column=2)
    
    value_text = tk.Text(tab1, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, c.hex_array_to_value(var_value))
    value_text.configure(state="normal")
    value_text.grid(row=row, column=3)

    variables_labels[var_name] = label
    variables_values[var_name] = value_text
    row += 1

Tem_labels = {}
Tem_values = {}

row = 1

for var_name, var_value in c.translate_battery_pram(c.pack_allTemperature, c.all_temperature).items():
    label = tk.Label(tab1, text=f"{var_name}:")
    label.grid(row=row, column=6)
    
    value_text = tk.Text(tab1, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, var_value)
    value_text.configure(state="disabled")
    value_text.grid(row=row, column=7)

    Tem_labels[var_name] = label
    Tem_values[var_name] = value_text
    row += 1


row = 1

Vol_labels = {}
Vol_values = {}


for var_name, var_value in c.translate_battery_pram(c.pack_allVoltage, c.all_voltage).items():
    label = tk.Label(tab1, text=f"{var_name}:")
    label.grid(row=row, column=4)
    
    value_text = tk.Text(tab1, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, var_value)
    value_text.configure(state="disabled")
    value_text.grid(row=row, column=5)

    Vol_labels[var_name] = label
    Vol_values[var_name] = value_text
    row += 1


row = 1 
col = 0
status_labels = {}
status_values = {}
status_dict = c.translate_Battery_status(c.status_, c.micro_status)

for var_name, var_value in status_dict.items():
    label = tk.Label(tab2, text=f"{var_name}:")
    label.grid(row=row, column=col)
    
    combobox = ttk.Combobox(tab2, values=[0, 1], width=2)
    combobox.grid(row=row, column=col+1)
    combobox.current(var_value)  # Set the initial value based on status_dict

    status_labels[var_name] = label
    status_values[var_name] = combobox

    if row == 23:  # Adjust the condition based on your layout
        col += 2
        row = 0
    
    row += 1

row = 1
col = 8

adc_labels = {}
adc_values = {}

for var_name, var_value in c.translate_battery_pram(c.adc, c.adc_vals).items():
    label = tk.Label(tab2, text=f"{var_name}:")
    label.grid(row=row, column=col)
    
    value_text = tk.Text(tab2, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, var_value)
    value_text.configure(state="normal")
    value_text.grid(row=row, column=col+1)

    adc_labels[var_name] = label
    adc_values[var_name] = value_text

    if(row == 23):
        col += 2
        row = 0
    row += 1

row = 3
col = 0
eeprom_labels = {}
eeprom_values = {}

for x in c.translate_eeprom_page(c.eeprom_page_data, c.eeprom_data):
    label = tk.Label(tab4, text=f"{x[0]}:")
    label.grid(row=row, column=col)
    
    value_text = tk.Text(tab4, wrap=tk.WORD, width=10, height=1)
    value_text.insert(tk.END, x[1])
    value_text.configure(state="normal")
    value_text.grid(row=row, column=col+1)

    eeprom_labels[x[0]] = label
    eeprom_values[x[0]] = value_text

    if(row == 23):
        col += 2
        row = 3
    row += 1


# Rest of your code
root.mainloop()