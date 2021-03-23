import sys
from socket import *

def scan(host, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        print('[+] %s -> %d open' % (host, port))
        s.close()
    except Exception as e:
        pass

def main(prefix, ports):
    setdefaulttimeout(0.3)
    for ip in range(0, 256):
        for port in map(int, ports.split(',')):
            scan('%s.%s' % (prefix, ip), port)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('python s.py 192.168.0 80,443')
