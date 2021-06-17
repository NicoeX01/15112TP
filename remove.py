#from 15-112 recursion file notes
import os
def removeTempFiles(path, suffix='.DS_Store'): 
    if path.endswith(suffix):
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTempFiles(path + '/' + filename, suffix)
removeTempFiles("music/", suffix='.DS_Store')