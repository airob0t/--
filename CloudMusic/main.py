#coding:utf-8
#author:AIRobot

from random import randint
import wave

#define of params
#NUM_SAMPLES = 2000
framerate = 16000
nframes = 32000
channels = 1
sampwidth = 2
#record time
TIME = 2
        
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes("".join(data))
    wf.close()
        
def rand(filename):
    data = ""
    for i in xrange(0,32000):
        data += str(randint(0,255))
    save_wave_file(filename,data)
        
if __name__ == '__main__':
    for i in xrange(1,1001):
        name = 'out/'+str(i)+'.wav'
        rand(name)
        print i
