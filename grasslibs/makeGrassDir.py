import os
import grasslibs.getMcDir as mcd

def makeGrassDir(dirExtension=[]):
    grassDir = os.path.join(mcd.getMcDir(), "grasslauncher")
    fullDir = os.path.join(grassDir, *dirExtension)
    if not os.path.isdir(fullDir):
        os.mkdir(fullDir)