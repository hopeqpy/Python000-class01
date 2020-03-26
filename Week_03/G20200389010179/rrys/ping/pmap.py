import sys, getopt
import os
import time
import queue
import threading
import subprocess
import telnetlib
import json
import datetime

class Pmap(object):
    def __init__(self):
        pass
    
    @classmethod
    def ping(self,ipaddr):
        num = 1
        wait = 1000
        ping = subprocess.Popen(f'ping -n {num} -w {wait} {ipaddr}',stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        exit_code = ping.wait()
        if exit_code != 0:
            print(f'{ipaddr} no ! ! !')
        else:
            print(f'{ipaddr} is link now!')
    
    @classmethod
    def telnetport(self,ipaddr,port):
        server = telnetlib.Telnet()
        try:
            server.open(ipaddr,port)
            print(f'{ipaddr} port {port} is open')
        except Exception as err:
            print(f'{ipaddr} port {port} is not open')
        finally:
            server.close()

def getipaddr(ipaddr):
        ipaddrcounts = []
        ipnum = 0
        ipaddr = ipaddr.split('-')
        ipfirst = ipaddr[0].split('.')
        startip = f'{ipfirst[0]}.{ipfirst[1]}.{ipfirst[2]}.'
        endip = ipaddr[0].split('.')[3]
        if ipaddr[1] != None:
            ipnum = int(ipaddr[1].split('.')[3]) - int(ipaddr[0].split('.')[3])

        ipaddrcounts = [ipaddr[0],ipnum,startip,endip]

        return ipaddrcounts

def writeinfo(f,info):
    f.write(json.dumps(info))

    
def check_ip(q,address):
    try:
        while True:
            ip = q.get_nowait()
            Pmap.ping(ip)
    except queue.Empty as e:
        pass

def check_port(q,ipaddr):
    try:
        while True:
            port = q.get_nowait()
            Pmap.telnetport(ipaddr,port)
    except queue.Empty as e:
        pass

def threadfunc(func,q,counts,address=None):
    threads = []
    for i in range(counts):
        t = threading.Thread(target=func,args=(q,address,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

def pingthread(ipaddr,counts):
    q = queue.Queue()
    iplist = getipaddr(ipaddr)
    ipfirst = iplist[0]
    ipstart = iplist[2]
    ipend = int(iplist[3])
    ipnum = int(iplist[1])
    for i in range(ipnum+1):
        q.put(f'{ipstart}{ipend}')
        ipend = ipend + 1
    
    threadfunc(check_ip,q,counts)

def testportthread(ipaddr,counts):
    q = queue.Queue()
    for i in range(0,65535):
        q.put(i)

    threadfunc(check_port,q,counts,ipaddr)
    


def main(argv):
   counts = ''
   testtype = ''
   ipaddr = ''
   try:
      opts, args = getopt.getopt(argv,"n:f:ip:",["counts=","func=","ip="])
   except getopt.GetoptError:
      print ('pmap.py -n <counts> -f <ping or tcp> -ip <ip address>')
      sys.exit(2)
   for opt, arg in opts:
      print(opt)
      if opt == '-h':
         print ('pmap.py -n <counts> -f <ping or tcp> -ip <ip address>')
         sys.exit()
      elif opt in ("-n", "--counts"):
         counts = int(arg)
      elif opt in ("-f", "--ping or tcp"):
         testtype = arg
      elif opt in ("--ip", "--ip address"):
         ipaddr = arg
         
   print(f'-n={counts}\t-f={testtype}\t-ip={ipaddr}')

   if testtype == 'ping':
       pingthread(ipaddr,counts)
   elif testtype == 'tcp':
       testportthread(ipaddr,counts) 
       
if __name__ == "__main__":
   main(sys.argv[1:])
   