import socket
import struct
import random
import sys

data_packet = 0
acknowledgement_packet = 1

class packet():
    '''the class that deals with making packets and reading and sending them'''
    def __init__(self, magicno, typ, seqno, datalen, data):
        self.magicno = magicno
        self.type = typ
        self.seqno = seqno
        self.datalen = datalen
        self.data = data

    def make_bytes(self):
        '''makes the packet sendable and turns it into bytes'''
        header = struct.pack('iiii', self.magicno, self.type, self.seqno, self.datalen)
        body = self.data
        packet = header + body
        return packet

    @classmethod
    def from_bytes(cls, bytes):
        '''makes the packet from the bytes'''
        header, body = bytes[:16], bytes[16:]
        magicno, typ, seqno, datalen = struct.unpack('iiii', header)
        return cls(magicno, typ, seqno, datalen, body)

try:
    csin = int(sys.argv[1])
    csout = int(sys.argv[2])
    crin = int(sys.argv[3])
    crout = int(sys.argv[4])
    sin = int(sys.argv[5])
    rin = int(sys.argv[6])
    precision = float(sys.argv[7])
except:
    print(sys.argv)
    print("Port numbers must be integers")

def main(csin, csout, crin, crout, sin, rin, precision):
    '''sets up sockets and starts loop'''
    if (csin <= 1024 or csin >= 64000) and (csout <= 1024 or csout >= 64000) and \
        (crin <= 1024 or crin >= 64000) and (crout <= 1024 or crout >= 64000):
        print("port numbers not within range", csin, csout, crin, crout)
        return("bad")
    if precision > 1 or precision < 0:
        print("precision is not in range", precision)
        return("bad")
#set up sockets
    sock_csin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crsin.bind(('127.0.0.1', csin))

    sock_csout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_csout.bind(('127.0.0.1', csout))
    sock_csout.connect(('127.0.0.1', sin))

    sock_crin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crin.bind(('127.0.0.1', crin))

    sock_crout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crout.bind(('127.0.0.1', crout))
    sock_crout.connect(('127.0.0.1', rin))

#inifinite loop waits of input
    random.seed()
    while True:

        packeti, addressi = sock_csin.recvfrom(1024)
        drop = input_received(sock_csin, sock_crout, packeti)
        if drop == "dropped":
            continue

        packetr, addressr = sock_crin.recvfrom(1024)
        drop = input_received(sock_rsin, sock_csout, packetr)
        if drop == "dropped":
            break


def input_received(recieved_into, forward_to, packet):
    '''determines whether to drop the packet and sends it on'''
    magicno, typ, seqno, datalen, body = packet.from_bytes(packet)
    u = random.uniform(0, 1)
    if magicno != 0x497E or u < precision:
        return "dropped"
    else:
        recieved_into.sendto(packeti, ('127.0.0.1', forward_to))
        packeti, addressi = forward_to.recvfrom(1024)
        forward_to.send(packeti)


if __name__ == "__main__":
    main()
