import os

def makeGrassDir(dirExtension=[]):
    grassDir = os.path.join(os.environ["HOME"], ".minecraft", "grasslauncher")
    fullDir = os.path.join(grassDir, *dirExtension)
    if not os.path.isdir(fullDir):
        os.mkdir(fullDir)