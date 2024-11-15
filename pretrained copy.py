# from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
# from essentia.standard import TensorflowPredictMusiCNN
# import numpy as np

# def getGenre(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MTG Genre Classifier.pb")
#     predictions = model(embeddings)

#     data = [
#         "60s", "70s", "80s", "90s", "acidjazz", "alternative", "alternativerock", "ambient", "atmospheric", "blues", 
#         "bluesrock", "bossanova", "breakbeat", "celtic", "chanson", "chillout", "choir", "classical", "classicrock", 
#         "club", "contemporary", "country", "dance", "darkambient", "darkwave", "deephouse", "disco", "downtempo", 
#         "drumnbass", "dub", "dubstep", "easylistening", "edm", "electronic", "electronica", "electropop", "ethno", 
#         "eurodance", "experimental", "folk", "funk", "fusion", "groove", "grunge", "hard", "hardrock", "hiphop", 
#         "house", "idm", "improvisation", "indie", "industrial", "instrumentalpop", "instrumentalrock", "jazz", 
#         "jazzfusion", "latin", "lounge", "medieval", "metal", "minimal", "newage", "newwave", "orchestral", "pop", 
#         "popfolk", "poprock", "postrock", "progressive", "psychedelic", "punkrock", "rap", "reggae", "rnb", "rock", 
#         "rocknroll", "singersongwriter", "soul", "soundtrack", "swing", "symphonic", "synthpop", "techno", "trance", 
#         "triphop", "world", "worldfusion"
#     ]
#     genre_labels = data
#     # calculate average probability of all frames for each genre
#     average_predictions = np.mean(predictions, axis=0)
#     top = np.argsort(average_predictions)[-1]
#     top_genre = genre_labels[top]
#     return top_genre

# # Milion Song Dataset
# def getGenreMillion(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Genre.pb", input="serving_default_model_Placeholder", output="PartitionedCall")
#     predictions = model(embeddings)

#     data = [
#         "rock", "pop", "alternative", "indie", "electronic", "female vocalists", "dance", "00s", "alternative rock", 
#         "jazz", "beautiful", "metal", "chillout", "male vocalists", "classic rock", "soul", "indie rock", "Mellow", 
#         "electronica", "80s", "folk", "90s", "chill", "instrumental", "punk", "oldies", "blues", "hard rock", 
#         "ambient", "acoustic", "experimental", "female vocalist", "guitar", "Hip-Hop", "70s", "party", "country", 
#         "easy listening", "sexy", "catchy", "funk", "electro", "heavy metal", "Progressive rock", "60s", "rnb", 
#         "indie pop", "sad", "House", "happy"
#     ]
  
#     genre_labels = data
#     # calculate average probability of all frames for each genre
#     average_predictions = np.mean(predictions, axis=0)
#     top = np.argsort(average_predictions)[-1]
#     top_genre = genre_labels[top]
#     return top_genre

# def getEngagement(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Engagement.pb", output="model/Identity")
#     predictions = model(embeddings)
#     # return the mean of each frame's popularity and penalize a large STD
#     return np.mean(predictions) - np.std(predictions)

# def getPopularity(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Approachability.pb", output="model/Identity")
#     predictions = model(embeddings)
#     # return the mean of each frame's popularity and penalize a large STD
#     return np.mean(predictions) - np.std(predictions)

# def getVA(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Valence Arousal.pb", output="model/Identity")
#     predictions = model(embeddings)
#     valence = np.mean([i[0] for i in predictions])
#     arousal = np.mean([i[1] for i in predictions])
#     return (valence,arousal)
   
# def getDanceability(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Danceability.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     d = np.mean([i[0] for i in predictions])
#     nd = np.mean([i[1] for i in predictions])
#     return (d,nd)

# def getMoodGroup(filename):
#     # try catch
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Mood Group.pb", input="serving_default_model_Placeholder",
#                                 output="PartitionedCall")
#     try:
#         predictions = model(embeddings)
#     except TypeError:
#         print("Oops! TypeError getting mood group")
#         return ''

#     data = {
#         "classes": [
#             "passionate, rousing, confident, boisterous, rowdy",
#             "rollicking, cheerful, fun, sweet, amiable/good natured",
#             "literate, poignant, wistful, bittersweet, autumnal, brooding",
#             "humorous, silly, campy, quirky, whimsical, witty, wry",
#             "aggressive, fiery, tense/anxious, intense, volatile, visceral"
#         ]
#     }
#     theme_labels = data["classes"]
    
#     average_predictions = np.mean(predictions, axis=0)
#     top = np.argsort(average_predictions)[-1]
#     return theme_labels[top]

# def getAggressive(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)
#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Aggressive.pb", output="model/Softmax")
#     predictions = model(embeddings)

#     # return the average confidence that it is aggressive or non
#     agg = np.mean([i[0] for i in predictions])
#     non = np.mean([i[1] for i in predictions])
#     return (agg,non)

# def getHappy(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)
#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Happy.pb", output="model/Softmax")
#     predictions = model(embeddings)

#     # return the average confidence that it is aggressive or non
#     hap = np.mean([i[0] for i in predictions])
#     non = np.mean([i[1] for i in predictions])
#     return (hap,non)

# def getRelaxed(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)
#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Relax.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     # return the average confidence that it is aggressive or non
#     rel = np.mean([i[0] for i in predictions])
#     non = np.mean([i[1] for i in predictions])
#     return (rel,non)

# def getSad(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)
#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Sad.pb", output="model/Softmax")
#     predictions = model(embeddings)

#     # return the average confidence that it is aggressive or non
#     sad = np.mean([i[0] for i in predictions])
#     non = np.mean([i[1] for i in predictions])
#     return (sad,non)

# #bright/dark
# def getTimbre(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="essentia graphfiles/Discogs Effnet BS64 Model.pb",
#                                                      output="PartitionedCall:1")
#     embeddings = embedding_model(audio)
#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/Effnet Timbre.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     bright = np.mean([i[0] for i in predictions])
#     dark = np.mean([i[1] for i in predictions])
#     return (bright,dark)

# def getAcoustic(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Acoustic.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     ac = np.mean([i[0] for i in predictions])
#     notac = np.mean([i[1] for i in predictions])
#     return (ac,notac)

# def getElectronic(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Electronic.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     el = np.mean([i[0] for i in predictions])
#     notel = np.mean([i[1] for i in predictions])
#     return (el,notel)

# def getInstrumental(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Instrumental.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     inst = np.mean([i[0] for i in predictions])
#     notinst = np.mean([i[1] for i in predictions])
#     return (inst,notinst)

# def getGender(filename):
#     audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()
#     embedding_model = TensorflowPredictMusiCNN(graphFilename="essentia graphfiles/MusicNN embed.pb", output="model/dense/BiasAdd")
#     embeddings = embedding_model(audio)

#     model = TensorflowPredict2D(graphFilename="essentia graphfiles/MNN Gender.pb", output="model/Softmax")
#     predictions = model(embeddings)
#     f = np.mean([i[0] for i in predictions])
#     m = np.mean([i[1] for i in predictions])
#     return (m,f)