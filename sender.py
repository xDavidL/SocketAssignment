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
        c_s_in = int(sys.argv[3])
        file_name = sys.argv[4]
    except(Exception):
        print("Port numbers must be integers (sender)")
        return 1
    if len({port_in, port_out, c_s_in}) != 3:
        print("port numbers must be unique")
        return 2
    if 1024 >= port_in >= 64000 or 1024 >= port_out >= 64000:
        print("Ports numbers must be between 1024 and 64000 (sender)")
        return 3

    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    try:
        s_in.bind((local_host, port_in))
        s_out.bind((local_host, port_out))
    except Exception as e:
        print(e)
        print("Port/s are already in use (sender)")
        s_in.close()
        s_out.close()
        return 4

    s_out.connect((local_host, c_s_in))

    if not os.path.isfile(file_name):
        print("File", file_name,  "does not exist.(sender)")
        s_in.close()
        s_out.close()
        return 4

    f = open(file_name, 'rb')
    seq_num = 0
    exit_flag = False
    packets_sent = 0
    #termination_count = 0
    while not exit_flag:
        data = f.read(512)
        data_len = len(data)
        if data_len == 0:
            buff_packet = Packet(MAGICNO, DATA_PACKET, seq_num, data_len, None)
            packet_buffer = buff_packet.make_bytes()
            exit_flag = True
        else:
            buff_packet = Packet(MAGICNO, DATA_PACKET, seq_num, data_len, data)
            packet_buffer = buff_packet.make_bytes()

        while True:
            # if exit_flag:
            #     termination_count += 1
            #     if termination_count >= 10:
            #         break
            try:
                s_out.send(packet_buffer)
            except Exception as e:
                print(e)
                print("Sender could not send data to channel")
                f.close()
                s_in.close()
                s_out.close()
                return 5
            packets_sent += 1
            recvd, _, _ = select.select([s_in], [], [], 1)
            if s_in in recvd:
                packet = s_in.recv(1024)
                magicno, typ, seqno, datalen, body = from_bytes(packet)
                if typ != ACKNOWLEDGEMENT_PACKET or \
                                    magicno != MAGICNO or \
                                    datalen != 0:
                    continue
                if seqno == seq_num:
                    seq_num = 1 - seq_num
                    if exit_flag:
                        print("Packets Sent: " + str(packets_sent))
                    break
    f.close()
    s_in.close()
    s_out.close()
    return 0


if __name__ == "__main__":
    main()
