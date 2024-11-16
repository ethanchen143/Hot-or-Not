import random
# actual essentia prediction are not used because essentia can't be installed in the docker container

def getGenre(filename):
    return "pop"

def getGenreMillion(filename):
    return "electronic"

def getEngagement(filename):
    return 0.62

def getPopularity(filename):
    return 0.44

def getVA(filename):
    return (5.3, 4.4)

def getDanceability(filename):
    return (0.92,0.08)

def getMoodGroup(filename):
    return "rollicking, cheerful, fun, sweet, amiable/good natured"

def getAggressive(filename):
    return (0.04,0.96)

def getHappy(filename):
    return (0.32,0.68)

def getRelaxed(filename):
    return (0.42,0.58)

def getSad(filename):
    return (0.85,0.15)

def getTimbre(filename):
    return (0.48,0.52)

def getAcoustic(filename):
    return (0.01,0.99)

def getElectronic(filename):
    return (0.96, 0.04)

def getInstrumental(filename):
    return (0.02, 0.98)

def getGender(filename):
    return (0.19, 0.81)