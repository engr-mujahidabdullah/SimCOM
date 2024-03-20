import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
from Packet import ParsedPacket
from Battery import Battery
import serial.tools.list_ports
import threading
import time

class BatteryApp:
    def __init__(self, master):
        self.master = master
        self.c = Battery()
        self.pack = ParsedPacket()
        self.ser = None
        self.reading_data = False
        self.variables_values = {}

        self.create_widgets()
        self.refresh_com_ports()

    def create_widgets(self):
        # Create and configure the tkinter widgets
        self.com_port_label = tk.Label(self.master, text="Select COM Port:")
        self.com_port_var = tk.StringVar()
        self.com_port_dropdown = ttk.Combobox(self.master, textvariable=self.com_port_var)
        self.refresh_button = tk.Button(self.master, text="Refresh COM", command=self.refresh_com_ports)
        self.open_port_button = tk.Button(self.master, text="Open Port", command=self.open_port)
        self.close_port_button = tk.Button(self.master, text="Close Port", command=self.close_port, state=tk.DISABLED)
        self.received_data_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=120, height=10)

        # Place widgets in the window
        self.com_port_label.grid(row=0, column=0)
        self.com_port_dropdown.grid(row=0, column=1)
        self.refresh_button.grid(row=0, column=2)
        self.open_port_button.grid(row=0, column=3)
        self.close_port_button.grid(row=0, column=4)
        self.received_data_text.grid(row=25, column=0, columnspan=12, rowspan=10)

    def refresh_com_ports(self):
        available_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.com_port_dropdown['values'] = available_ports
        self.com_port_var.set(available_ports[0])  # Set the default COM port

    def open_port(self):
        selected_port = self.com_port_var.get()
        try:
            self.ser = serial.Serial(selected_port, 4800, parity=serial.PARITY_EVEN)
            self.received_data_text.insert(tk.END, f"Port {selected_port} is opened.\n")
            self.open_port_button.config(state=tk.DISABLED)
            self.close_port_button.config(state=tk.NORMAL)
            self.reading_data = True
            data_thread = threading.Thread(target=self.read_serial_data)
            data_thread.daemon = True
            data_thread.start()
        except Exception as e:
            self.received_data_text.insert(tk.END, f"Error: {str(e)}\n")

    def close_port(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            self.received_data_text.insert(tk.END, f"Port {self.ser.port} is closed.\n")
            self.open_port_button.config(state=tk.NORMAL)
            self.close_port_button.config(state=tk.DISABLED)
            self.reading_data = False
        else:
            self.received_data_text.insert(tk.END, "No open port to close.\n")

    def read_serial_data(self):
        try:
            while self.reading_data:
                # Read and process serial data
                time.sleep(0.1)  # Simulate reading data
                self.master.update()  # Update the GUI
        except Exception as e:
            print(e)
            self.close_port()
            self.open_port()

    # Add other methods for sending data, updating GUI, etc.

# Create the tkinter application
app = tk.Tk()
app.title("Battery Communication App")

# Initialize and run the BatteryApp
battery_app = BatteryApp(app)
app.mainloop()
