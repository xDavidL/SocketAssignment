import socket

class Packet():
    def __init__(magicno, type, seqno, datalen, data):
        self.magicno = magicno
        self.type = type
        self.seqno = seqno
        self.datalen = datalen
        self.data = data

def channel(csin, csout, crin, crout, sin, rin, precision):

    if (csin <= 1024 or csin >= 64000) and (csout <= 1024 or csout >= 64000) and (crin <= 1024 or crin >= 64000) and (crout <= 1024 or crout >= 64000):
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
    sock_csout.connect(('127.0.0.1', csout))

    sock_crin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crin.bind(('127.0.0.1', crin))

    sock_crout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crout.bind(('127.0.0.1', crout))
    sock_crout.connect(('127.0.0.1', crout))

#inifinite loop waits of input

    while True:

        packet, address = sock_csin.recvfrom(1024)
        packet, address = sock_crin.recvfrom(1024)

#whren input recieved :
        #checks magicno feild
        #channel decided if it should drop Packet
        #send packet on
