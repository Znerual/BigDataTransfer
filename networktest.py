from scapy.arch import IFACES
from scapy.layers.inet import *
import urllib.request
from scapy.sendrecv import send, sniff
from random import randint

class Connection:
    def __init__(self):
        self.seq_A = 1
        self.seq_B = 0



DESTINATION_HOST = "194.232.104.142"  #"80.110.70.170"
DESTINATION_PORT = 80

SOURCE_PORT = randint(1024,65535)
SOURCE_HOST = "192.168.0.31"

interfaces = []
for key, value in IFACES.items():
    if not "[Unknown]" in str(value):
        interfaces.append(value)
        print(f"key {key} value {value}")

def match_packet(pkt):
    #pkt.show()
    if pkt.haslayer(IP) and pkt[IP].dst == SOURCE_HOST \
            and pkt.haslayer(TCP) and pkt[TCP].dport == SOURCE_PORT:
            #and pkt[TCP].ack == self.seq_next:
        return True
    return False

#create a TCL Handshake
#SYN
ip = IP(dst=DESTINATION_HOST)
SYN = TCP(sport=SOURCE_PORT, dport=DESTINATION_PORT, flags='S', seq=1000)
synAck = sr1(ip/SYN)
#send(ip/SYN)
#ans = sniff(iface=interfaces,lfilter=match_packet,count=6,timeout=10)
#ans.show()
synAck.show()
#SYNACK =sr1(ip/SYN) #send the package and wait for the answer


#ACK
#ACK = TCP(sport=SOURCE_PORT, dport=DESTINATION_PORT, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
#send(ip/ACK)

print(f"Source port {SOURCE_PORT}")