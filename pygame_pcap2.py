#!/usr/bin/env python2

import pygame
import pcap
import sys
import string
import time
import socket
import struct

protocols={socket.IPPROTO_TCP:'tcp',
           socket.IPPROTO_UDP:'udp',
           socket.IPPROTO_ICMP:'icmp'}

def decode_ip_packet(s):
  d={}
  d['version']=(ord(s[0]) & 0xf0) >> 4
  d['header_len']=ord(s[0]) & 0x0f
  d['tos']=ord(s[1])
  d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
  d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
  d['flags']=(ord(s[6]) & 0xe0) >> 5
  d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
  d['ttl']=ord(s[8])
  d['protocol']=ord(s[9])
  d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
  d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
  d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
  if d['header_len']>5:
    d['options']=s[20:4*(d['header_len']-5)]
  else:
    d['options']=None
  d['data']=s[4*d['header_len']:]
  return d

def print_packet(pktlen, data, timestamp):
  if not data:
    return

  if data[12:14]=='\x08\x00':
    decoded=decode_ip_packet(data[14:])
    try:
        stat_data[decoded['source_address']] += 1
    except KeyError:
        stat_data[decoded['source_address']] = 1
    try:
        stat_data[decoded['destination_address']] -= 1
    except KeyError:
        stat_data[decoded['destination_address']] = -1
    print '%s > %s' % (decoded['source_address'],
                             decoded['destination_address'])
    print len(stat_data.keys())
 

if __name__=='__main__':

  if len(sys.argv) < 3:
    print 'usage: sniff.py <interface> <expr>'
    sys.exit(0)
  p = pcap.pcapObject()
  #dev = pcap.lookupdev()
  dev = sys.argv[1]
  net, mask = pcap.lookupnet(dev)
  # note:  to_ms does nothing on linux
  p.open_live(dev, 1600, 0, 100)
  #p.dump_open('dumpfile')
  p.setfilter(string.join(sys.argv[2:],' '), 0, 0)

  # try-except block to catch keyboard interrupt.  Failure to shut
  # down cleanly can result in the interface not being taken out of promisc.
  # mode
  #p.setnonblock(1)
  stat_data = {}
  try:
    surface = pygame.display.set_mode((600,600))
    pygame.init()
    while 1:
      p.dispatch(1, print_packet)
      surface.fill(0)
      width = int(surface.get_width() / (len(stat_data.keys()) + 2))
      x = width
      y_zero = int(surface.get_height() / 2)
      for (key, value) in stat_data.items():
        print key, value
        color = pygame.Color(0, 0, 0)
        color.hsva = (value % 360, 100, 100, 4)
        pygame.draw.rect(surface, color, (x, y_zero - value, width, value))
        x += width
      pygame.display.update()
  except KeyboardInterrupt:
    print '%s' % sys.exc_type
    print 'shutting down'
    print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()
