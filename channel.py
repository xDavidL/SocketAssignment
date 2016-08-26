import socket
import struct
import random
import sys
import select

data_packet = 0
acknowledgement_packet = 1

class Packet():
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
        if self.data != None:
            body = self.data
            packet = header + body
        else:
            packet = header
        return packet

    #@classmethod
def from_bytes(bytes):
    '''makes the packet from the bytes'''
    header, body = bytes[:16], bytes[16:]
    magicno, typ, seqno, datalen = struct.unpack('iiii', header)
    return [magicno, typ, seqno, datalen, body]


def main():

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
    sock_csin.bind(('127.0.0.1', csin))
    #sock_csin.connect(('127.0.0.1', crout))

    sock_csout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_csout.bind(('127.0.0.1', csout))
    sock_csout.connect(('127.0.0.1', sin))

    sock_crin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crin.bind(('127.0.0.1', crin))
    #sock_crin.connect(('127.0.0.1', csout))

    sock_crout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock_crout.bind(('127.0.0.1', crout))
    sock_crout.connect(('127.0.0.1', rin))

#inifinite loop waits of input
    random.seed()
    while True:
        #selct https://pymotw.com/2/select/
        #readable, writable, exceptional = select.select([sock_csin, sock_crin], [sock_csout, sock_crout], [sock_csin, sock_crin, sock_csout, sock_crout], 1)
        readable, writable, exceptional = select.select([sock_csin, sock_crin], [sock_csout, sock_crout], [sock_csin, sock_crin, sock_csout, sock_crout], 5)

        if sock_csin in readable:

            packeti, addressi = sock_csin.recvfrom(1024)
          #  sock_csin.sendto(packeti, addressi);
            #print("packet received from sender = ", from_bytes(packeti), addressi)

            drop = input_received(packeti, precision)

            if drop == "dropped":
                continue
            else:

                sock_crout.send(packeti)
            #    print("channel send on to receiver", packeti)

        if sock_crin in readable:
            packetr, addressr = sock_crin.recvfrom(1024)
            #print("Received confirmation packets from receiver = ", from_bytes(packetr), addressr)
            drop = input_received(packetr, precision)
            if drop == "dropped":
                continue
            else:

                sock_csout.send(packetr)
                #print("channel sent on acknowledgement_packet to sender ", packeti)
    print("Closing channel sockets")
    sock_csin.close()
    sock_csout.close()
    sock_crin.close()
    sock_crout.close()


def input_received(packet, precision):
    '''determines whether to drop the packet and sends it on'''
    magicno, typ, seqno, datalen, body = from_bytes(packet)
    u = random.uniform(0, 1)
    if magicno != 0x497E or u < precision:
        #print("DROPPED !!!!", magicno)
        return "dropped"
    return 0
  #  else:
       # recieved_into.sendto(packet, ("127.0.0.1", forward_to_port))
       # print("line 1 :^(")
        #packet = forward_to.recv(1024)
    #    print("line 1 :^)")
      #  forward_to.send(packet)
      #  print("SENTT !!!!  12344")


if __name__ == "__main__":
    main()
