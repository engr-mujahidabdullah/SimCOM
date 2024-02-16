from Charger import Charger
from Packet import ParsedPacket

#c = Charger()
#pack = ParsedPacket()

#p = pack.min_CRC16()
#print(p)
#pack.parse_received_packet([0xff, 0x55, 0x00, 0x2f, 0x02, 0x00, 0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x20, 0x17, 0x70, 0x00, 0x00, 0x07, 0xd0, 0x0f, 0xa0, 0x09, 0xc4, 0x00, 0x00, 0x07, 0xd0, 0x00, 0x00, 0x01, 0xf4, 0x00, 0x00, 0x3a, 0x98, 0x21, 0x34, 0x17, 0x70, 0x20, 0xd0, 0x00, 0x00, 0x2e, 0x7c, 0xac, 0xa4])
#pack.packet_attributes()
#data = [0x17, 0x70, 0x00, 0x00, 0x07, 0xD0, 0x0F, 0xA0, 0x09, 0xC4, 0x00, 0x00, 0x07, 0xD0, 0x00, 0x00, 0x01, 0xF4, 0x00, 0x00, 0x3A, 0x98, 0x21, 0x34, 0x17, 0x70, 0x20, 0xD0, 0x00, 0x00, 0x2E, 0x7C]
#c.data_parser([0x02, 0x00], pack.data)
#c.charger_attributes()
#c.status = [0x0f, 0xf0]
#k = c.translate_Charger_status()
#print(k)

import secrets

def generate_random():
    return secrets.token_bytes(16)

def compare_random(R1, R2):
    if(R1 == R2):
        return False
    else:
        return True
    
def generate_code(Rand, IV, pwd):
    return (IV + pwd) * Rand

def compare_code(code1, code2):
    if(code1 == code2):
        return True
    else:
        return False

#define function
def HLS_I(IV, pwd):
    #generate Random R1 and send
    r1 = generate_random()

    #receive Random R2
    r2 = generate_random()

    if(compare_random(r1, r2)):

        #GMAC R2
        c2 = generate_code(r2, IV, pwd)
        #send Result c2
        #get Result c2r
        c2r = generate_code(r2, IV, pwd) #received code
        #compare 1
        if(compare_code(c2, c2r)):
            #GMAC R1
            c1 = generate_code(r1, IV, pwd)
            #send result c1
            #get result c1r
            c1r = generate_code(r1, IV, pwd)
            #compare 2
            if(compare_code(c1, c1r)):
                return True 
    return False

#define function
def HLS_II(IV, pwd):
    #generate Random R1 and send
    r1 = generate_random()

    #receive Random R2
    r2 = generate_random()

    if(compare_random(r1, r2)):

        #GMAC R2
        c2 = generate_code(r2, IV, pwd)
        #GMAC R1
        c1 = generate_code(r1, IV, pwd)
        #send Result c2
        #get Result c2r
        c2r = generate_code(r2, IV, pwd) #received code
        #compare 1
        if(compare_code(c2, c2r)):
            #send and get result c1r
            c1r = generate_code(r1, IV, pwd) #received code
            #compare 2
            if(compare_code(c1, c1r)):
                return True  
    return False