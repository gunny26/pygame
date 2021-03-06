#!/usr/bin/python

import urllib2
import time
import pygame
import sys


SCREEN = (640,480)
FPS = 0.5

class GraphData:
    """Holds Data for graphics display with pygame"""
    
    def __init__(self, length, height):
        "just __init__"
        self.length = length
        self.height = height
        # length is the maximim length of dataset
        self.data = [0] * length
        # height ist the maximum allowed size of the grafics
        # autoscale max(data) = height
        self.first = True
        self.last_data = None

    def add(self, data):
        "adds new data to end of list"
        # if first_data is None, store value in last_data only
        if self.first is True:
            self.last_data = data
            self.first = False
        else:
            # remove first
            self.data.pop(0)
            # append to end, but only difference to last data
            self.data.append(data - self.last_data)
            self.last_data = data
        # print self.data

    def get_data(self, off_y=0):
        "returns normalized Dataset to draw with pygame.draw.polygon"
        gauge_data = self.data
        maximum = max(gauge_data)
        print "maximum in dataset", maximum
        plot_data = []
        counter = 0
        for data in gauge_data:
            if maximum > 0:
                plot_data.append((counter, off_y - data * self.height / maximum))
            else:
                plot_data.append((counter, off_y - 0))
            counter += 1
        plot_data.append((self.length, 0))
        return(plot_data)

def get_haproxy_csv(top_level_url, url, username, password):
    # for basic authentication
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # add authentication information
    password_mgr.add_password(None, top_level_url, username, password)
    # create handler
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    # create opener
    opener = urllib2.build_opener(handler)
    # open url
    res = opener.open(url)
    csv = res.read().split('\n')
    return(csv)

def csv_to_dict(csv):
    """
    converts csv data into dict with key pxname_svname
    in fist row column names
    """
    col_string = csv[0]
    # replace leading "# " with nothing
    col_string.replace("^# ", '')
    cols = col_string.split(',')
    # print cols
    # remove first line
    csv.pop(0)
    # dict to hold data
    hadata = {}
    for row in csv:
        values = row.split(',')
        # on last line, no data, so continue
        if len(values) != len(cols):
            continue
        # print values
        key = "%s_%s" % (values[0], values[1])
        # dict holds dict
        hadata[key] = {}
        # counter get column number
        counter = 0
        for value in values:
            hadata[key][cols[counter]] = value
            counter += 1
        # data finished
        # print hadata[key]
    return(hadata)

def draw_grid(surface, color, step_x, step_y):
    for x in range(0, surface.get_width(), step_x):
        pygame.draw.line(surface, color, (x, 0), (x, surface.get_height()), 1)
    for y in range(0, surface.get_height(), step_y):
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y), 1)

def get_data(hadata, pxname, svname, key):
    return(hadata["%s_%s" % (pxname, svname)][key])
 
def main(top_level_url, url, username, password):
    # initialize pygame
    surface = pygame.display.set_mode(SCREEN)
    pygame.init()
    graph_data=GraphData(640, 480)
    clock = pygame.time.Clock()
    # graph_data = numpy.zeros(640, numpy.dtint))
    while True:
        csv = get_haproxy_csv(top_level_url, url, username, password)
        # something like this
        # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,
        # lb01,FRONTEND,,,1,1,2000,15,2928,38936,0,0,0,,,,,OPEN,,,,,,,,,1,1,0,,,,0,2,0,2,
        # print csv
        # print type(csv)
        hadata = csv_to_dict(csv)
        print hadata
        # print hadata
        data = int(get_data(hadata, "static", "BACKEND", "bout"))
        print "lb01 FRONTEND bout:", data
        graph_data.add(data)
        points = graph_data.get_data(int(surface.get_height() / 2))
        # print points

        # pygame stuff
        # blank screen
        surface.fill((0,0,0))
        draw_grid(surface, (100, 100, 100), 10, 10)
        pygame.draw.aalines(surface, (255, 0, 0), False, points, 1)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    url_base = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    main(url_base, "%s/haproxy?stats;csv" % url_base, username, password)
