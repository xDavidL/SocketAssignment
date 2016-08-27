#!/usr/bin/python3

import socket
import sys
import os

import select
from channel import Packet, from_bytes

DATA_PACKET = 0
ACKNOWLEDGEMENT_PACKET = 1
MAGICNO = 0x497E


def main():
    try:
        port_in = int(sys.argv[1])
        port_out = int(sys.argv[2])
        c_r_in = int(sys.argv[3])
        file_name = sys.argv[4]
    except:
        #print("receiver syss.args", sys.argv)
        print("Port numbers must be integers (receiver)")
        sys.exit(1)
    if len({port_in, port_out, c_r_in}) != 3:
        print("Port numbers must be unique")
    if 1024 >= port_in >= 64000 or 1024 >= port_out >= 64000:
        print("Ports numbers must be between 1024 and 64000 (receiver)")
        sys.exit(2)

    #print(0)

    r_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    r_in.bind((local_host, port_in))
    r_out.bind((local_host, port_out))
    r_out.connect((local_host, c_r_in))

    #if os.path.isfile(file_name):
        #print("File already exists.")
        #r_in.close()
        #r_out.close()
        #sys.exit(3)

    f = open(file_name, 'w')
    expected = 0
    while True:

# something about a blocking call needs to be implemented
        #recvd, address = r_in.recvfrom(1024)
        #from_bytes(recvd)
        readable, _, _ = select.select([r_in], [], [], 1)


# dont know how to determine if there is a response or not
        #print(" In the receiver ")

        if r_in in readable:
            packet = r_in.recv(1024)

            magicno, typ, seqno, datalen, body = from_bytes(packet)
            if typ != DATA_PACKET or \
                                magicno != MAGICNO:
            #    print("receiver incorrect arguments")
                continue

            
            if seqno != expected:
                #print("receiver incorrect seqno", expected, seqno)
                ackno_packet = Packet(MAGICNO, ACKNOWLEDGEMENT_PACKET, seqno, 0, None)
                ackno_packet = ackno_packet.make_bytes()
                r_out.send(ackno_packet)
        #        print("receiver send ACKNOWLEDGEMENT_PACKET")
                continue
            else:
            #    print("receiver correct seqno",  expected, seqno)
                #print("receiver got correct packet of ")
                ackno_packet = Packet(MAGICNO, ACKNOWLEDGEMENT_PACKET, seqno, 0, None)
                ackno_packet = ackno_packet.make_bytes()
                r_out.send(ackno_packet)
            #    print("receiver send ACKNOWLEDGEMENT_PACKET")
                expected = 1 - expected
                f.write(body.decode("utf-8"))
            if datalen == 0:
                f.close()
                r_in.close()
                r_out.close()
                break

            #print(body.decode("utf-8"))






if __name__ == "__main__":
    main()
