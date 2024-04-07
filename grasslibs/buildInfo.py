import platform
import sys
import os
import grasslibs.getMcDir as mcd

def getBuildSpecs():
    pythonVersion = sys.version
    system = platform.platform()
    grassLaunchDir = os.path.join(mcd.getMcDir(), "grasslauncher")
    toReturn = f'''
Info:

Python version: {pythonVersion}
Os: {system}
Grass Launch directory: {grassLaunchDir}
'''
    return toReturn