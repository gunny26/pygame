#!/usr/bin/python
import mad
import ao
import sys

mf = mad.MadFile(sys.argv[1])
dev = ao.AudioDevice('alsa', rate=mf.samplerate())
while 1:
    buf = mf.read()
    if buf is None:
        break
    dev.play(buf, len(buf))
