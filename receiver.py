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
        print("Port numbers must be integers (receiver)")
        return 1
    if len({port_in, port_out, c_r_in}) != 3:
        print("Port numbers must be unique")
        return 2
    if 1024 >= port_in >= 64000 or 1024 >= port_out >= 64000:
        print("Ports numbers must be between 1024 and 64000 (receiver)")
        return 3

    r_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    r_in.bind((local_host, port_in))
    r_out.bind((local_host, port_out))
    r_out.connect((local_host, c_r_in))

    if os.path.isfile(file_name):
        print("File already exists.")
        r_in.close()
        r_out.close()
        return 4

    f = open(file_name, 'w')
    expected = 0
    while True:
        readable, _, _ = select.select([r_in], [], [], 1)
        if r_in in readable:
            packet = r_in.recv(1024)
            magicno, typ, seqno, datalen, body = from_bytes(packet)
            if typ != DATA_PACKET or magicno != MAGICNO:
                continue
            if seqno != expected:
                ackno_packet = Packet(MAGICNO, ACKNOWLEDGEMENT_PACKET, seqno, 0, 
                        None)
                ackno_packet = ackno_packet.make_bytes()
                try:
                    r_out.send(ackno_packet)
                except Exception as e:
                    print(e)
                    print("Receiver could not sent acknowledgement to channel")
                    f.close()
                    r_in.close()
                    r_out.close()
                    return 5
                continue
            else:
                ackno_packet = Packet(MAGICNO, ACKNOWLEDGEMENT_PACKET, seqno, 0, 
                        None)
                ackno_packet = ackno_packet.make_bytes()
                try:
                    r_out.send(ackno_packet)
                except Exception as e:
                    print(e)
                    print("Receiver could not sent acknowledgement to channel")
                    f.close()
                    r_in.close()
                    r_out.close()
                    return 5
                expected = 1 - expected
                f.write(body.decode("utf-8"))
            if datalen == 0:
                f.close()
                r_in.close()
                r_out.close()
                return 0



if __name__ == "__main__":
    main()
