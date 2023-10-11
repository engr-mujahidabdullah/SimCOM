'''
Includes
'''
import serial
from data_check import parityGenerator as parity

pg = parity()

x = pg.data_P([118])
print(x)
#print(type(x))
print(pg.break_data(x))
print(pg.is_valid_parity(x))

