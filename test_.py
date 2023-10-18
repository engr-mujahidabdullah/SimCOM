from data_check import CRC16
x = CRC16()

data2 = [0xff, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00]

result_crc = x.min_CRC16(data2)
print("CRC-16:", hex(result_crc))
