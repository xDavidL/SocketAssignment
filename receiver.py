#!/usr/bin/python3

import socket
import sys
import os

from select import select
from channel import packet

def main():
    try:
        args = [int(x) for x in sys.argv[1:-1]] + [sys.argv[-1]]
        print(args)
    except(Exception):
        print("Port numbers must be integers")
        sys.exit(1)
    if 1024 >= args[0] >= 64000 or 1024 >= args[1] >= 64000:
        print("Ports numbers must be between 1024 and 64000")
        sys.exit(2)

    print(0)

    r_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    r_in.bind((local_host, args[0]))
    r_out.bind((local_host, args[1]))
    r_out.connect((local_host, args[2]))

    print(args[3])

    if os.path.isfile(args[3]):
        print("File already exists.")
        s_in.close()
        s_out.close()
        sys.exit(3)

    f = open(args[3], 'w')
    while True:
        expected = 0
# something about a bolcking call needs to be implemented
        recvd, address = r_in.recvfrom(1024)
        if recvd.magicno != 0x497E or recvd.type != "data_packet":
            continue
        ack_pack = packet(0x497E, "acknowledgement_packet", recvd.seqno, 0)
        r_out.send(ack_pack)
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
