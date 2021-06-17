from cmu_112_graphics import *
import time, random    
from aubio import source,onset 
from pygame import mixer
from bpm import bpmDetection
#music from https://www.youtube.com/watch?v=quGq98wQqKI&list=PL27cDFtN1Uv8dOZFwr5wnNV9qPVAOmXOn

#from 112 website 
def almostEqual(d1, d2, epsilon=10**-2.1): #from 15-112 website 
    return (abs(d2 - d1) < epsilon)

################################################################################
#from aubio demo github  https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
class Onset(object):
    def __init__(self,path):
        self.path=path

    def getOnsetTimes(self): #returns list of onset times 
        win_s = 1024//2       # fft size
        hop_s = win_s // 2    # hop size: number of samples between each successive FFT window

        filename = self.path
        samplerate = 44100
        s = source(filename, samplerate, hop_s) #creates source object (iterable) 
        samplerate = s.samplerate

        o = onset("default", win_s, hop_s, samplerate)

        # list of onsets, in samples
        onsets = []

        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()
            if o(samples):
                onsets.append(float("%f" % o.get_last_s()))

            total_frames += read
            if read < hop_s: break #reached end of the file 
        return onsets

sound=Onset("A Dance of Fire and Ice.wav")
#print(sound.getOnsetTimes()) 

def make_beat(l):
    res = []
    hello = dict()
    for i in range(1, len(l)):
        diff = round(l[i] - l[i-1], 2)
        res.append(diff)
        hello[diff] = hello.get(diff, 0) + 1
    print(res)
    #print(hello)
    multi = []
    for i in range (0, len(res)):
        multi.append(round((res[i] / 0.2), 3))
    #print(multi)
    return multi

lstMulti=make_beat(sound.getOnsetTimes())


#0.4, 0.8, 0.4, 0.75, 0.35, 0.4, 0.4, 0.4, 0.4, 0.35, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]
#filter alg (not all beats returned by onsetTime detector are beats)
# go through multiplier list, see if it's any value in the note list
# yes: append to filtered list 
# no: search for values to add so that it becomes one of the values in the note list 
#     add values to the filtered list 
# if can't find and hit one of the notes, round to nearest note and add to filtered list 

standMulti = [8,4,2,3,1.5,1,0.5] #standard beat multipliers (8th note is 1)
def filter(lstMulti,standMulti): #return filtered list of onset beat multipliers  
    res=[]
    i=0
    while i!=len(lstMulti):
        currEle=lstMulti[i]
        if currEle in standMulti:
            res.append(currEle)
            i+=1

        else: #starts searching for values to add 
            j=i+1
            total=0
            while lstMulti[j] not in standMulti and total<=max(standMulti):
                total+=currEle + lstMulti[j]
                if total in standMulti:
                    #print(i,j,total,lstMulti[i:j+1])
                    res.append(total)
                    i=j+1
                    break
                j+=1

            # did not find anything --> round to neareast multi in standMulti
            diff=[]
            for targ in standMulti:
                diff.append(abs(total-targ)) 
            closestIndex=diff.index(min(diff))
            closest=standMulti[closestIndex]
            #print(i,j,total,closest,lstMulti[i:j+1])
            res.append(closest)
            i=j+1
    return res
