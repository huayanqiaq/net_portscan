#!/usr/bin/python
# coding:utf-8

"""
@author: cike
@time: 2019/6/16 13:48
"""
import optparse
from socket import *
from threading import *
import time


screenLock = Semaphore(value=1)
# threadinglist = []
resultlist = []


def ip2num(ip):
    ip=[int(x) for x in ip.split('.')]
    return ip[0] <<24 | ip[1]<<16 | ip[2]<<8 |ip[3]

def num2ip(num):
    return '%s.%s.%s.%s' %( (num & 0xff000000) >>24,(num & 0x00ff0000) >>16,(num & 0x0000ff00) >>8,
 num & 0x000000ff )

def get_ip(ip):
    start,end = [ip2num(x) for x in ip.split('-') ]
    return [ num2ip(num) for num in range(start,end+1) if num & 0xff ]

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        #connSkt.settimeout(100)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('cikepython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print('[+]%s:%d/tcp open' % (tgtHost,tgtPort))
        print('[+] ' + str(results))
        str1 = "%s,%s,%s\r\n" %(tgtHost,str(tgtPort),results.replace('\n','').replace('\r',''))
        resultlist.append(str1)

    except:
        screenLock.acquire()
        print('[-]%d/tcp close' % (tgtPort))
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHosts, tgtPorts):
    setdefaulttimeout(100)
    for tgtHost in tgtHosts:
        for tgtPort in tgtPorts:
            t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
            t.start()
            # threadinglist.append(t)

def main():
    parser = optparse.OptionParser('usage%prog ' + '-h <taget Host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='input host string')
    parser.add_option('-p', dest='tgtPorts', type='string', help='input ports list string')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPorts).split(',')
    tgtHosts = get_ip(tgtHost)
    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    # tgtHosts = ['111.230.154.42']
    # tgtPorts = ['3306']
    portScan(tgtHosts, tgtPorts)
    time.sleep(3)
    for result in resultlist:
        with open('cike.csv','a') as f:
            f.write(result)


if __name__ == '__main__':
    main()
