#!/usr/bin/python3

import socket
import sys
import os

import select
from channel import Packet, from_bytes

data_packet = 0
acknowledgement_packet = 1


def main():
    try:
        port_in = int(sys.argv[1])
        port_out = int(sys.argv[2])
        c_r_in = int(sys.argv[3])
        file_name = sys.argv[4]
    except:
        print("receiver syss.args", sys.argv)
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
        readable, _, _ = select.select([r_in], [], [], 5)


# dont know how to determine if there is a response or not
        print(" In the receiver ")

        if r_in in readable:
            packet = r_in.recv(1024)

            magicno, typ, seqno, datalen, body = from_bytes(packet)
        #    print("receiver got packet of     ", magicno, typ, seqno, datalen, body)
            if typ != data_packet or \
                                magicno != 0x497E:
            #    print("receiver incorrect arguments")
                continue


            if seqno != expected:
            #    print("receiver incorrect seqno", expected, seqno)
                ackno_packet = Packet(0x497E, acknowledgement_packet, seqno, 0, body)
                ackno_packet = ackno_packet.make_bytes()
                r_out.send(ackno_packet)
        #        print("receiver send acknowledgement_packet")
                break
            else:
            #    print("receiver correct seqno",  expected, seqno)
                ackno_packet = Packet(0x497E, acknowledgement_packet, seqno, 0, None)
                ackno_packet = ackno_packet.make_bytes()
                r_out.send(ackno_packet)
            #    print("receiver send acknowledgement_packet")
                expected = 1 - expected
            if datalen == 0:
                f.close()
                r_in.close()
                r_out.close()
                break

            #print(body.decode("utf-8"))
            f.write(body.decode("utf-8"))






if __name__ == "__main__":
    main()
