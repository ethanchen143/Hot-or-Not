import random

def getGenre(filename):
    data = [
        "60s", "70s", "80s", "90s", "acidjazz", "alternative", "alternativerock", "ambient", "atmospheric", "blues", 
        "bluesrock", "bossanova", "breakbeat", "celtic", "chanson", "chillout", "choir", "classical", "classicrock", 
        "club", "contemporary", "country", "dance", "darkambient", "darkwave", "deephouse", "disco", "downtempo", 
        "drumnbass", "dub", "dubstep", "easylistening", "edm", "electronic", "electronica", "electropop", "ethno", 
        "eurodance", "experimental", "folk", "funk", "fusion", "groove", "grunge", "hard", "hardrock", "hiphop", 
        "house", "idm", "improvisation", "indie", "industrial", "instrumentalpop", "instrumentalrock", "jazz", 
        "jazzfusion", "latin", "lounge", "medieval", "metal", "minimal", "newage", "newwave", "orchestral", "pop", 
        "popfolk", "poprock", "postrock", "progressive", "psychedelic", "punkrock", "rap", "reggae", "rnb", "rock", 
        "rocknroll", "singersongwriter", "soul", "soundtrack", "swing", "symphonic", "synthpop", "techno", "trance", 
        "triphop", "world", "worldfusion"
    ]
    # Return random genre
    return random.choice(data)

def getGenreMillion(filename):
    data = [
        "rock", "pop", "alternative", "indie", "electronic", "female vocalists", "dance", "00s", "alternative rock", 
        "jazz", "beautiful", "metal", "chillout", "male vocalists", "classic rock", "soul", "indie rock", "Mellow", 
        "electronica", "80s", "folk", "90s", "chill", "instrumental", "punk", "oldies", "blues", "hard rock", 
        "ambient", "acoustic", "experimental", "female vocalist", "guitar", "Hip-Hop", "70s", "party", "country", 
        "easy listening", "sexy", "catchy", "funk", "electro", "heavy metal", "Progressive rock", "60s", "rnb", 
        "indie pop", "sad", "House", "happy"
    ]
    # Return random genre
    return random.choice(data)

def getEngagement(filename):
    # Return random value between -1 and 1
    return random.uniform(-1, 1)

def getPopularity(filename):
    # Return random value between -1 and 1
    return random.uniform(-1, 1)

def getVA(filename):
    # Return random valence and arousal between -1 and 1
    return (random.uniform(-1, 1), random.uniform(-1, 1))

def getDanceability(filename):
    # Return random probabilities that sum to 1
    d = random.random()
    return (d, 1-d)

def getMoodGroup(filename):
    moods = [
        "passionate, rousing, confident, boisterous, rowdy",
        "rollicking, cheerful, fun, sweet, amiable/good natured",
        "literate, poignant, wistful, bittersweet, autumnal, brooding",
        "humorous, silly, campy, quirky, whimsical, witty, wry",
        "aggressive, fiery, tense/anxious, intense, volatile, visceral"
    ]
    return random.choice(moods)

def getAggressive(filename):
    # Return random probabilities that sum to 1
    agg = random.random()
    return (agg, 1-agg)

def getHappy(filename):
    # Return random probabilities that sum to 1
    hap = random.random()
    return (hap, 1-hap)

def getRelaxed(filename):
    # Return random probabilities that sum to 1
    rel = random.random()
    return (rel, 1-rel)

def getSad(filename):
    # Return random probabilities that sum to 1
    sad = random.random()
    return (sad, 1-sad)

def getTimbre(filename):
    # Return random probabilities that sum to 1
    bright = random.random()
    return (bright, 1-bright)

def getAcoustic(filename):
    # Return random probabilities that sum to 1
    ac = random.random()
    return (ac, 1-ac)

def getElectronic(filename):
    # Return random probabilities that sum to 1
    el = random.random()
    return (el, 1-el)

def getInstrumental(filename):
    # Return random probabilities that sum to 1
    inst = random.random()
    return (inst, 1-inst)

def getGender(filename):
    # Return random probabilities that sum to 1
    m = random.random()
    return (m, 1-m)