import scipy
import scipy.fftpack
import pylab
from scipy import pi
import pyaudio
import numpy
import time
import pygame

t = scipy.linspace(0,120,4000)
acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t) + 2*scipy.random.random(len(t))
# acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t)

signal = acc(t)

def record():
    p = pyaudio.PyAudio()
    t1 = time.time() 
    inStream = p.open(format=pyaudio.paInt16,
        channels=1, rate=8192,\
        input=True, output=True)
    pcm=abs(numpy.fromstring(inStream.read(4000), dtype=numpy.int16))
    t2 = time.time()
    return(pcm)
 

pygame.init()
surface = pygame.display.set_mode(320, 200)

#t1 = time.time()
#signal = record()
#t2 = time.time() - t1
#t = scipy.linspace(0, t2, 4000)
print "Signal"
print signal
print len(signal)
FFT = abs(scipy.fft(signal))
print "FFT transformed Signal"
print FFT
print len(FFT)
freqs = abs(scipy.fftpack.fftfreq(signal.size, t[1]-t[0]))
print "Frequencies"
print freqs
print len(freqs)
while True:
    pygame.draw.line(surface, (255, 255, 255), (0, 0, 100, 100))
    pygame.display.update()
pylab.subplot(211)
pylab.plot(t, signal)
pylab.subplot(212)
pylab.plot(freqs,20*scipy.log10(FFT),'x')
pylab.show()
