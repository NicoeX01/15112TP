from aubio import source, tempo
import statistics

#from aubio gibhub demo (replaced numpy in beats_to_bpm): 
# https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
class bpmDetection():
    def __init__(self,path):
        self.path=path

    def get_file_bpm(self):
        # Calculate beats per minute (bpm) of a given file.
        # path: path to the file
    
        samplerate, win_s, hop_s = 44100, 1024, 512 #default 

        s = source(self.path, samplerate, hop_s) #creates aubio objeect 
        samplerate = s.samplerate  #gets samplerate 
        o = tempo() #built-in aubio function; gets a list of beats
        # List of beats (times), in samples
        beats = []
        # Total number of frames read
        total_frames = 0

        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
            total_frames += read
            if read < hop_s: #reached end of the file 
                break
        return bpmDetection.beats_to_bpm(beats, self.path)

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms=[]
            #replaced numpy diff and median with for loop and statistics.median() 
            for i in range(len(beats)-1):
                bpms.append(60/(beats[i+1]-beats[i]))
            return int(statistics.median(bpms))  
        else:
            print("not enough beats found in {:s}".format(path))
            return 0
