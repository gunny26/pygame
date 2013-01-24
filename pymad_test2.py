#!/usr/bin/python
import pyaudio
import mad
import sys

if len(sys.argv) < 2:
    print "Plays a wave file.\n\n" +\
          "Usage: %s filename.wav" % sys.argv[0]
    sys.exit(-1)

mf = mad.MadFile(sys.argv[1])

p = pyaudio.PyAudio()

# open stream
stream = p.open(format =
                p.get_format_from_width(pyaudio.paInt32),
                channels = 2,
                rate = mf.samplerate(),
                output = True)

# read data
data = mf.read()

# play stream
while data != None:
    stream.write(data)
    data = mf.read()

stream.close()
p.terminate()
