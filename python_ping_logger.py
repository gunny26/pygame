#!/usr/bin/python

import os
import socket
socket.setdefaulttimeout(1000)
import select
import sys
import random
import time

# receive Timeout in Seconds
recv_timeout = 1

def main(dest_name, logfilename):
    logfile = open(logfilename, "wb")
    headline = "#time\tduration\tmin\tavg_60\tavg_300\tmax\taddress"
    print headline
    logfile.write(headline + "\n")
    dest_addr = socket.gethostbyname(dest_name)
    port = random.randint(1, 65535)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    # send_socket.setsockopt(socket.SOL_IP)
    recv_socket.bind(("", port))
    curr_addr = None
    curr_name = None
    min_value = 99.0
    max_value = 0.0
    avg_60 = 0.0
    avg_300 = 0.0
    while True:
        starttime = time.time()
        duration = 0
        send_socket.sendto("", (dest_name, port))
        try:
            recv_socket.setblocking(0)
            # set receive timeout in seconds
            ready = select.select([recv_socket], [], [], recv_timeout)
            if ready[0]:
                _, curr_addr = recv_socket.recvfrom(512)
                duration = time.time() - starttime
                curr_addr = curr_addr[0]
                if duration > max_value : max_value = duration
                if duration < min_value : min_value = duration
                avg_60 = (59 * avg_60 + duration) / 60
                avg_300 = (299 * avg_300 + duration) / 300
                output = "%d\t%0.8f\t%0.8f\t%0.8f\t%0.8f\t%0.8f\t%s" % (starttime, duration, min_value, avg_60, avg_300, max_value, curr_addr)
                print output
                logfile.write(output+"\n")
                logfile.flush()
            else:
                print "%d Timeout waiting for response" % starttime
        except socket.error:
            pass
        time.sleep(1)
    send_socket.close()
    recv_socket.close()
    logfile.close()

if __name__ == "__main__":
    logfilename = os.path.abspath("./python_ping_logger.py").split(".")[0] + ".log"
    main(sys.argv[1], logfilename)
