from pygame import mixer 
#from 112 pygame audio https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        mixer.init()
        mixer.music.load(path)
        mixer.music.set_volume(0.5)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        mixer.music.stop()
    def pause(self):
        mixer.music.pause()
    def unpause(self):
        mixer.music.unpause()
    def isPlaying(self):
        return bool(mixer.music.get_busy())
    def getLength(self):
        return mixer.music.get_length(self.path)

