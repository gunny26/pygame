import pygame
import numpy
import threading
import pyaudio
import scipy
import scipy.fftpack
import scipy.io.wavfile
import wave
import sys

rate=8000 #try 5000 for HD data, 48000 for realtime
soundcard=11
windowWidth=500
fftsize=512
currentCol=0
scooter=[]
overlap=5 #1 for raw, realtime - 8 or 16 for high-definition
def graphFFT(pcm):
        global currentCol, data
        ffty=scipy.fftpack.fft(pcm) #convert WAV to FFT
        ffty=abs(ffty[0:len(ffty)/2])/500 #FFT is mirror-imaged
        #ffty=(scipy.log(ffty))*30-50 # if you want uniform data
        # print "MIN:\t%s\tMAX:\t%s"%(min(ffty),max(ffty))
        for i in range(len(ffty)):
                if ffty[i]<0: ffty[i]=0
                if ffty[i]>255: ffty[i]=255
        scooter.append(ffty)
        if len(scooter)<6:return
        scooter.pop(0)
        ffty=(scooter[0]+scooter[1]*2+scooter[2]*3+scooter[3]*2+scooter[4])/9
        data=numpy.roll(data,-1,0)
        data[-1]=ffty[::-1]
        currentCol+=1
        if currentCol==windowWidth: currentCol=0
        
def record():
        p = pyaudio.PyAudio() 
        inStream = p.open(format=pyaudio.paInt16,channels=1,rate=rate,\
                                                input=True, output=True)
        linear=[0]*fftsize
        while True:
                linear=linear[fftsize/overlap:]
                pcm=numpy.fromstring(inStream.read(fftsize/overlap), dtype=numpy.int16)
                linear=numpy.append(linear,pcm)
                graphFFT(linear)
                
pal = [(max((x-128)*2,0),x,min(x*2,255)) for x in xrange(256)] 
print max(pal),min(pal)
data=numpy.array(numpy.zeros((windowWidth,fftsize/2)),dtype=int)
#data=Numeric.array(data) # for older PyGame that requires Numeric
pygame.init() #crank up PyGame
pygame.display.set_caption("Simple Spectrograph")
screen=pygame.display.set_mode((windowWidth,fftsize/2))
world=pygame.Surface((windowWidth,fftsize/2),depth=8) # MAIN SURFACE
world.set_palette(pal)
t_rec=threading.Thread(target=record) # make thread for record()
t_rec.daemon=True # daemon mode forces thread to quit with program
t_rec.start() #launch thread
clk=pygame.time.Clock()
while 1:
        for event in pygame.event.get(): #check if we need to exit
                if event.type == pygame.QUIT:pygame.quit();sys.exit()
        pygame.surfarray.blit_array(world,data) #place data in window
        screen.blit(world, (0,0))
        pygame.display.flip() #RENDER WINDOW
        clk.tick(30) #limit to 30FPS
