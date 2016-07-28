import socket
import sys
import os.path


def main():
    try:
        args = [int(x) for x in sys.argv[1:-1]] [sys.argv[-1]]
    except(Exception):
        print("Port numbers must be integers")
        sys.exit(1)
    
    if 1024 >= args[0] >= 64000 or 1024 >= args[1] >= 64000:
        print("Ports numbers must be between 1024 and 64000")
        sys.exit(2)
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_host = "127.0.0.1"
    s_in.bind((local_host, args[0]))
    s_out.bind((local_host, args[1]))
    s_out.connect((local_host, args[2]))
    
	if not os.path.isfile(args[3]):
		print("File does not exist.")
		sys.exit(3)
	
	next = 0
	exit_flag = false

	
