#!/usr/bin/python3

import socket
import sys
import os

from select import select
from channel import Packet, from_bytes

data_packet = 0
acknowledgement_packet = 1


def main():
    try:
        port_in = int(sys.argv[1])
        port_out = int(sys.argv[2])
        c_s_in = int(sys.argv[3])
        file_name = sys.argv[4]
    except:
        print(sys.argv)
        print("Port numbers must be integers(receiver)")
        sys.exit(1)
    if 1024 >= port_in >= 64000 or 1024 >= port_out >= 64000:
        print("Ports numbers must be between 1024 and 64000(receiver)")
        sys.exit(2)

    #print(0)

    r_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    r_in.bind((local_host, port_in))
    r_out.bind((local_host, port_out))
    r_out.connect((local_host, c_s_in))

    #if os.path.isfile(file_name):
        #print("File already exists.")
        #r_in.close()
        #r_out.close()
        #sys.exit(3)

    f = open(file_name, 'w')
    while True:
        expected = 0
# something about a bolcking call needs to be implemented
        recvd, address = r_in.recvfrom(1024)
        from_bytes(recvd)
        print("receiver !!! recvd =", recvd, address)
        
        if recvd.magicno != 0x497E or recvd.type != data_packet:
            continue
        ackno_packet = packet(0x497E, acknowledgement_packet, recvd.seqno, 0)
        ackno_packet = ackno_packet.make_bytes()
        r_out.send(ackno_packet)
        if recvd.seqno != expected:
            continue
        expected = 1 - expected
        if recvd.datalen == 0:
            f.close()
            r_in.close()
            r_out.close()
            sys.exit(0)
# probably have to do some decoding stuff here
        f.write(recvd.data)




if __name__ == "__main__":
    main()
