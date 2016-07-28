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


    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    s_in.bind((local_host, args[0]))
    s_out.bind((local_host, args[1]))
    s_out.connect((local_host, args[2]))


    print(args[3])


    if not os.path.isfile(args[3]):
        print("File does not exist.")
        s_in.close()
        s_out.close()
        sys.exit(3)



    print(2)


    with open(args[3], 'rb') as f:
        seq_num = 0
        exit_flag = False
        packets_sent = 0
        while not exit_flag:
            data = f.read(512)
            data_len = len(data)
            if data_len == 0:
                buff_packet = package(0x497E, "data_packet", seq_num, \
                                                                data_len, None)
                exit_flag = True
            else:
                buff_packet = packet(0x497E, "data_packet", seq_num, \
                                                                data_len, None)
                seq_num += 1


            while True:
                s_out.send(buff_packet)
                packets_sent += 1
                select.select([s_in], [], [], 1)
                if no_response:
                    continue
                elif recvd.type != "acknowledgement_packet" or \
                                    recvd.magicno != 0x497E or \
                                    recvd.dataLen != 0:
                    continue
                elif rcvd.seqno == seq_num:
                    seq_num = 1 - seq_num
                    if exit_flag:
                        print("Packets Sent: " + str(packets_sent))
                        f.close()
                        s_in.close()
                        s_out.close()
                        sys.exit(0)
                    break
    s_in.close()
    s_out.close()


if __name__ == "__main__":
    main()
