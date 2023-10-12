'''
Includes
'''
import serial
from data_check import parityGenerator, CRC16

pg = CRC16()

x = pg.data_crc(0xA4E0303A10040203)
print(x)
print(pg.check_crc16(x))

