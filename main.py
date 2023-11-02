from Charger import Charger
from Packet import ParsedPacket

c = Charger()
pack = ParsedPacket()

#p = pack.min_CRC16()
#print(p)
pack.parse_received_packet([0xff, 0x55, 0x00, 0x2f, 0x02, 0x00, 0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x20, 0x17, 0x70, 0x00, 0x00, 0x07, 0xd0, 0x0f, 0xa0, 0x09, 0xc4, 0x00, 0x00, 0x07, 0xd0, 0x00, 0x00, 0x01, 0xf4, 0x00, 0x00, 0x3a, 0x98, 0x21, 0x34, 0x17, 0x70, 0x20, 0xd0, 0x00, 0x00, 0x2e, 0x7c, 0xac, 0xa4])
pack.packet_attributes()
#data = [0x17, 0x70, 0x00, 0x00, 0x07, 0xD0, 0x0F, 0xA0, 0x09, 0xC4, 0x00, 0x00, 0x07, 0xD0, 0x00, 0x00, 0x01, 0xF4, 0x00, 0x00, 0x3A, 0x98, 0x21, 0x34, 0x17, 0x70, 0x20, 0xD0, 0x00, 0x00, 0x2E, 0x7C]
c.data_parser([0x02, 0x00], pack.data)
c.charger_attributes()