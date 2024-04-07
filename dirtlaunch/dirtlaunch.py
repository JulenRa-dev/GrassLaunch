import json
import os
import platform
from pathlib import Path
import subprocess


"""
Debug output
"""
def debug(str):
    if os.getenv('DEBUG') != None:
        print(str)

"""
[Gets the natives_string toprepend to the jar if it exists. If there is nothing native specific, returns and empty string]
"""
def get_natives_string(lib):
    arch = ""
    if platform.architecture()[0] == "64bit":
        arch = "64"
    elif platform.architecture()[0] == "32bit":
        arch = "32"
    else:
        raise Exception("Architecture not supported")

    nativesFile=""
    if not "natives" in lib:
        return nativesFile

    if "windows" in lib["natives"] and platform.system() == 'Windows':
        nativesFile = lib["natives"]["windows"].replace("${arch}", arch)
    elif "osx" in lib["natives"] and platform.system() == 'Darwin':
        nativesFile = lib["natives"]["osx"].replace("${arch}", arch)
    elif "linux" in lib["natives"] and platform.system() == "Linux":
        nativesFile = lib["natives"]["linux"].replace("${arch}", arch)
    else:
        raise Exception("Platform not supported")

    return nativesFile


"""
[Parses "rule" subpropery of library object, testing to see if should be included]
"""
def should_use_library(lib):
    def rule_says_yes(rule):
        useLib = None

        if rule["action"] == "allow":
            useLib = False
        elif rule["action"] == "disallow":
            useLib = True

        if "os" in rule:
            for key, value in rule["os"].items():
                os = platform.system()
                if key == "name":
                    if value == "windows" and os != 'Windows':
                        return useLib
                    elif value == "osx" and os != 'Darwin':
                        return useLib
                    elif value == "linux" and os != 'Linux':
                        return useLib
                elif key == "arch":
                    if value == "x86" and platform.architecture()[0] != "32bit":
                        return useLib

        return not useLib

    if not "rules" in lib:
        return True

    shouldUseLibrary = False
    for i in lib["rules"]:
        if rule_says_yes(i):
            return True

    return shouldUseLibrary

"""
[Get string of all libraries to add to java classpath]
"""
def get_classpath(lib, mcDir, version):
    cp = []

    for i in lib["libraries"]:
        if not should_use_library(i):
            continue

        libDomain, libName, libVersion = i["name"].split(":")[:3]
        jarPath = os.path.join(mcDir, "libraries", *
                               libDomain.split('.'), libName, libVersion)

        native = get_natives_string(i)
        jarFile = libName + "-" + libVersion + ".jar"
        if native != "":
            jarFile = libName + "-" + libVersion + "-" + native + ".jar"

        cp.append(os.path.join(jarPath, jarFile))
    if lib.get("jar"):
        cp.append(os.path.join(mcDir, "versions", lib["jar"], f"{lib['jar']}.jar"))
    else:
        cp.append(os.path.join(mcDir, "versions", version, f'{version}.jar'))

    return os.pathsep.join(cp)

def get_runtime(mcDir=str, trueVersion=str):
    runTim = "java-runtime-gamma"
    javaTrueName = "java"
    try:
        trueVersionInted = int(trueVersion)
        if trueVersionInted < 1.17:
            runTim = "jre-legacy"
    except:
        pass
    if platform.system().lower() == "windows":
        javaTrueName = "java.exe"
    return os.path.join(mcDir, "runtime", runTim, platform.system().lower(), runTim, "bin", javaTrueName)

def getMcDir():
    if platform.system().lower() == "windows":
        theoricalMcDir = os.path.join(os.getenv("APPDATA"), ".minecraft")
        if not os.path.isdir(theoricalMcDir):
            theoricalMcDir = os.path.join(os.getenv("LOCALAPPDATA"), ".minecraft")

    if platform.system().lower().startswith("linux"):
        theoricalMcDir = os.path.join(os.getenv("HOME"), ".minecraft")

    return theoricalMcDir

def launchVersion(version=str, account={}, uuid="{uuid}", accesToken="{token}"):
    version = version
    account = account
    uuid = uuid
    accessToken = accesToken

    mcDir = getMcDir()
    clientJson = json.loads(
        Path(os.path.join(mcDir, 'versions', version, f'{version}.json')).read_text())
    
    extraGameArgs = []
    extraJvmArgs = []
    crackedJvmArgs = []
    if not account["isMicrosoft"]:
        print("Not microsoft")
        crackedJvmArgs = [
            "-Dminecraft.api.env=custom",
            "-Dminecraft.api.auth.host=https://invalid.invalid",
            "-Dminecraft.api.account.host=https://invalid.invalid",
            "-Dminecraft.api.session.host=https://invalid.invalid",
            "-Dminecraft.api.services.host=https://invalid.invalid"
        ]
    trueVersion = clientJson["id"]
    if clientJson.get("inheritsFrom"):
        extraLibs = []
        inheritsFrom = json.loads(
            Path(os.path.join(mcDir, 'versions', clientJson["inheritsFrom"], f'{clientJson["inheritsFrom"]}.json')).read_text())
        extraLibs = inheritsFrom["libraries"]
        clientJson = inheritsFrom | clientJson
        clientJson["libraries"] += extraLibs
        extraGameArgs = clientJson["arguments"]["game"]
        trueVersion = inheritsFrom["id"]
        if clientJson.get("arguments").get("jvm"):
            extraJvmArgs = clientJson["arguments"]["jvm"]

    classPath = get_classpath(clientJson, mcDir, version)
    mainClass = clientJson['mainClass']
    versionType = clientJson['type']
    assetIndex = clientJson['assetIndex']['id']
    if "forge" in clientJson["id"]:
        print("Added args!")
        extraGameArgs = [
            "--tweakClass",
            "net.minecraftforge.fml.common.launcher.FMLTweaker",
            "--tweakClass",
            "net.minecraftforge.gradle.tweakers.CoremodTweaker"
        ]+extraGameArgs

    debug(classPath)
    debug(mainClass)
    debug(versionType)
    debug(assetIndex)

    runTim = get_runtime(mcDir, trueVersion)
    print(runTim)

    launchingArgs = [
        runTim,
        f'-Djava.library.path={classPath}',
        '-Dminecraft.launcher.brand=dirtlaunch-core',
        '-Dminecraft.launcher.version=2.1'
    ]+crackedJvmArgs+extraJvmArgs+[
        '-cp',
        classPath,
        mainClass,
        '--username',
        account['username'],
        '--version',
        version,
        '--gameDir',
        mcDir,
        '--assetsDir',
        os.path.join(mcDir, 'assets'),
        '--assetIndex',
        assetIndex,
        '--uuid',
        uuid,
        '--accessToken',
        accessToken,
        '--userType',
        'mojang',
        '--versionType',
        versionType
    ]+extraGameArgs
    
    subprocess.call(launchingArgs)

def launchPre16Version(version=str, username="Player", accesToken="{token}"):
    version = version
    username = username
    accessToken = accesToken

    mcDir = os.path.join(os.getenv('HOME'), '.minecraft')
    nativesDir = os.path.join(os.getenv('HOME'), 'versions', version, 'natives')
    clientJson = json.loads(
        Path(os.path.join(mcDir, 'versions', version, f'{version}.json')).read_text())
    classPath = get_classpath(clientJson, mcDir)
    mainClass = clientJson['mainClass']
    versionType = clientJson['type']
    assetIndex = clientJson['assetIndex']['id']

    debug(classPath)
    debug(mainClass)
    debug(versionType)
    debug(assetIndex)

    subprocess.call([
        '/usr/bin/java',
        f'-Djava.library.path={nativesDir}',
        '-Dminecraft.launcher.brand=dirtlaunch-core',
        '-Dminecraft.launcher.version=2.1',
        '-cp',
        classPath,
        'net.minecraft.client.Minecraft',
        username,
        accessToken,
    ])