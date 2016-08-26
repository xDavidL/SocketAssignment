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
        c_s_in = int(sys.argv[3])
        file_name = sys.argv[4]
    except(Exception):
        print("Port numbers must be integers (sender)")
        sys.exit(1)
    if 1024 >= port_in >= 64000 or 1024 >= port_out >= 64000:
        print("Ports numbers must be between 1024 and 64000(sender)")
        sys.exit(2)

    #print(0)

    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    s_in.bind((local_host, port_in))
    s_out.bind((local_host, port_out))
    s_out.connect((local_host, c_s_in))

    if not os.path.isfile(file_name):
        print("File does not exist.(sender)")
        s_in.close()
        s_out.close()
        sys.exit(3)

    #print(2)

    f = open(file_name, 'rb')
    seq_num = 0
    exit_flag = False
    packets_sent = 0
    while not exit_flag:
        data = f.read(512)
        data_len = len(data)
        if data_len == 0:
# some encoding / decoding might be necessary around here
            buff_packet = Packet(0x497E, data_packet, seq_num, data_len, None)
            packet_buffer = buff_packet.make_bytes()
            exit_flag = True
        else:
            buff_packet = Packet(0x497E, data_packet, seq_num, data_len, data)
            #print("This is buff_packet before make_bytes", buff_packet)
            packet_buffer = buff_packet.make_bytes()
            #print("This is buff_packet after make_bytes", buff_packet)


        while True:
        #    print("Sender send packed of ", packet_buffer)
            s_out.send(packet_buffer)
            packets_sent += 1
# dont know how select works/ dont know how to get the recvd packet
# select info https://pymotw.com/2/select/
            recvd, _, _ = select.select([s_in], [], [], 5)
# dont know how to determine if there is a response or not

            if s_in in recvd:
                packet = s_in.recv(1024)

                magicno, typ, seqno, datalen, body = from_bytes(packet)
                #print("sender confirmation received of ", magicno, typ, seqno, datalen, body)
                if typ != acknowledgement_packet or \
                                    magicno != 0x497E or \
                                    datalen != 0:
                    print("incorrect arguments")
                    continue
                print(seqno, seq_num)
                if seqno == seq_num:
                    print("seqno == correct")
                    seq_num = 1 - seq_num
                    if exit_flag:
                        print("Packets Sent: " + str(packets_sent))
                    break

    f.close()
    s_in.close()
    s_out.close()


if __name__ == "__main__":
    main()
