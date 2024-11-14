import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from pretrained import getGenre,getGenreMillion,getPopularity,getEngagement,getVA,getDanceability,getMoodGroup,getAggressive,getHappy,getRelaxed,getSad,getTimbre,getAcoustic,getElectronic,getGender,getInstrumental
import logging
import traceback

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

is_hot = 0
def extract_features(file_path):
    try:
        logger.info(f"Starting feature extraction for {file_path}")
        
        # Load audio file
        try:
            y, sr = librosa.load(file_path)
            logger.info("Audio loaded successfully with librosa")
        except Exception as e:
            logger.error(f"Failed to load audio file with librosa: {str(e)}")
            return None, f"Audio loading failed: {str(e)}"

        # Initialize feature array
        feature_list = []
        
        # Librosa Features
        try:
            logger.info("Starting librosa feature extraction...")
            
            # MFCC
            try:
                mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                mfccs_mean = np.mean(mfccs, axis=1)
                logger.info("MFCC extraction successful")
            except Exception as e:
                logger.error(f"MFCC extraction failed: {str(e)}")
                return None, f"MFCC extraction failed: {str(e)}"

            # Chroma STFT
            try:
                chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
                chroma_stft_mean = np.mean(chroma_stft, axis=1)
                logger.info("Chroma STFT extraction successful")
            except Exception as e:
                logger.error(f"Chroma STFT extraction failed: {str(e)}")
                return None, f"Chroma STFT extraction failed: {str(e)}"

            # Spectral Features
            try:
                spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
                spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
                spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

                spectral_centroid_mean = np.mean(spectral_centroid)
                spectral_bandwidth_mean = np.mean(spectral_bandwidth)
                spectral_contrast_mean = np.mean(spectral_contrast, axis=1)
                spectral_rolloff_mean = np.mean(spectral_rolloff)
                logger.info("Spectral features extraction successful")
            except Exception as e:
                logger.error(f"Spectral features extraction failed: {str(e)}")
                return None, f"Spectral features extraction failed: {str(e)}"

            # Rhythm Features
            try:
                tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
                zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
                logger.info("Rhythm features extraction successful")
            except Exception as e:
                logger.error(f"Rhythm features extraction failed: {str(e)}")
                return None, f"Rhythm features extraction failed: {str(e)}"

            # Tonnetz
            try:
                y_harmonic = librosa.effects.harmonic(y)
                tonnetz = librosa.feature.tonnetz(y=y_harmonic, sr=sr)
                tonnetz_mean = np.mean(tonnetz, axis=1)
                logger.info("Tonnetz features extraction successful")
            except Exception as e:
                logger.error(f"Tonnetz extraction failed: {str(e)}")
                return None, f"Tonnetz extraction failed: {str(e)}"

            logger.info("All librosa features extracted successfully")

        except Exception as e:
            logger.error(f"Overall librosa feature extraction failed: {str(e)}")
            return None, f"Librosa feature extraction failed: {str(e)}"

        # Essentia Features
        try:
            logger.info("Starting Essentia feature extraction...")
            
            try:
                genre = getGenre(file_path)
                logger.info("Genre extraction successful")
            except Exception as e:
                logger.error(f"Genre extraction failed: {str(e)}\n{traceback.format_exc()}")
                return None, f"Genre extraction failed: {str(e)}"

            try:
                genrem = getGenreMillion(file_path)
                logger.info("Genre Million extraction successful")
            except Exception as e:
                logger.error(f"Genre Million extraction failed: {str(e)}")
                return None, f"Genre Million extraction failed: {str(e)}"

            try:
                pop = getPopularity(file_path)
                logger.info("Popularity extraction successful")
            except Exception as e:
                logger.error(f"Popularity extraction failed: {str(e)}")
                return None, f"Popularity extraction failed: {str(e)}"

            try:
                eng = getEngagement(file_path)
                logger.info("Engagement extraction successful")
            except Exception as e:
                logger.error(f"Engagement extraction failed: {str(e)}")
                return None, f"Engagement extraction failed: {str(e)}"

            try:
                valence, arousal = getVA(file_path)
                logger.info("Valence/Arousal extraction successful")
            except Exception as e:
                logger.error(f"Valence/Arousal extraction failed: {str(e)}")
                return None, f"Valence/Arousal extraction failed: {str(e)}"

            try:
                dan, notdan = getDanceability(file_path)
                logger.info("Danceability extraction successful")
            except Exception as e:
                logger.error(f"Danceability extraction failed: {str(e)}")
                return None, f"Danceability extraction failed: {str(e)}"

            try:
                mgroup = getMoodGroup(file_path)
                logger.info("Mood Group extraction successful")
            except Exception as e:
                logger.error(f"Mood Group extraction failed: {str(e)}")
                return None, f"Mood Group extraction failed: {str(e)}"

            try:
                agg, notagg = getAggressive(file_path)
                logger.info("Aggressiveness extraction successful")
            except Exception as e:
                logger.error(f"Aggressiveness extraction failed: {str(e)}")
                return None, f"Aggressiveness extraction failed: {str(e)}"

            try:
                happy, nothappy = getHappy(file_path)
                logger.info("Happiness extraction successful")
            except Exception as e:
                logger.error(f"Happiness extraction failed: {str(e)}")
                return None, f"Happiness extraction failed: {str(e)}"

            try:
                relax, notrelax = getRelaxed(file_path)
                logger.info("Relaxed extraction successful")
            except Exception as e:
                logger.error(f"Relaxed extraction failed: {str(e)}")
                return None, f"Relaxed extraction failed: {str(e)}"

            try:
                sad, notsad = getSad(file_path)
                logger.info("Sadness extraction successful")
            except Exception as e:
                logger.error(f"Sadness extraction failed: {str(e)}")
                return None, f"Sadness extraction failed: {str(e)}"

            try:
                bright, dark = getTimbre(file_path)
                logger.info("Timbre extraction successful")
            except Exception as e:
                logger.error(f"Timbre extraction failed: {str(e)}")
                return None, f"Timbre extraction failed: {str(e)}"

            try:
                acou, notacou = getAcoustic(file_path)
                logger.info("Acoustic extraction successful")
            except Exception as e:
                logger.error(f"Acoustic extraction failed: {str(e)}")
                return None, f"Acoustic extraction failed: {str(e)}"

            try:
                elec, notelec = getElectronic(file_path)
                logger.info("Electronic extraction successful")
            except Exception as e:
                logger.error(f"Electronic extraction failed: {str(e)}")
                return None, f"Electronic extraction failed: {str(e)}"

            try:
                inst, vocal = getInstrumental(file_path)
                logger.info("Instrumental extraction successful")
            except Exception as e:
                logger.error(f"Instrumental extraction failed: {str(e)}")
                return None, f"Instrumental extraction failed: {str(e)}"

            try:
                male, female = getGender(file_path)
                logger.info("Gender extraction successful")
            except Exception as e:
                logger.error(f"Gender extraction failed: {str(e)}")
                return None, f"Gender extraction failed: {str(e)}"

            logger.info("All Essentia features extracted successfully")

        except Exception as e:
            logger.error(f"Overall Essentia feature extraction failed: {str(e)}")
            return None, f"Essentia feature extraction failed: {str(e)}"

        # Combine all features
        try:
            features = np.concatenate([
                [file_path.split('.mp3')[0].split('/')[-1]],  # filename
                [0],  # placeholder for is_hot
                [genre], [genrem], [pop], [eng], [valence], [arousal],
                [dan], [notdan], [mgroup], [agg], [notagg], [happy],
                [nothappy], [sad], [notsad], [relax], [notrelax],
                [bright], [dark], [acou], [notacou], [elec], [notelec],
                [inst], [vocal], [male], [female],
                mfccs_mean, chroma_stft_mean,
                [spectral_centroid_mean], [spectral_bandwidth_mean],
                spectral_contrast_mean, [spectral_rolloff_mean],
                [tempo], [zero_crossing_rate], tonnetz_mean
            ])
            logger.info("Features combined successfully")
            return features, None

        except Exception as e:
            error_msg = f"Feature combination failed: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return None, error_msg

    except Exception as e:
        error_msg = f"Unexpected error in feature extraction: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return None, error_msg

# def process_directory(directory_path):
#     feature_list = []
#     for file_name in tqdm(os.listdir(directory_path)):
#         if file_name.endswith('.mp3'):
#             file_path = os.path.join(directory_path, file_name)
#             features, error = extract_features(file_path)
#             if features is not None:
#                 feature_list.append(features)
#             else:
#                 logger.error(f"Error in feature extraction for {file_path}: {error}")
    
#     # Create a DataFrame with the features
#     column_names = [
#         'name', 'is_hot', 'genre', 'style', 'popularity', 'engagement', 'valence', 'arousal', 'danceable', 'not_danceable',
#         'mood_group', 'aggressive', 'not_aggressive', 'happy', 'not_happy', 'sad', 'not_sad', 'relaxing', 'not_relaxing',
#         'bright', 'dark', 'acoustic', 'not_acoustic', 'electronic', 'not_electronic', 'instrumental', 'vocal', 'male', 'female',
#         'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13',
#         'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5', 'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11', 'chroma_12',
#         'spectral_centroid', 'spectral_bandwidth', 'spectral_contrast_1', 'spectral_contrast_2', 'spectral_contrast_3', 'spectral_contrast_4', 'spectral_contrast_5', 'spectral_contrast_6', 'spectral_contrast_7',
#         'spectral_rolloff', 'tempo', 'zero_crossing_rate',
#         'tonnetz_1', 'tonnetz_2', 'tonnetz_3', 'tonnetz_4', 'tonnetz_5', 'tonnetz_6'
#     ]
#     features_df = pd.DataFrame(feature_list, columns=column_names)
#     return features_df

if __name__ == '__main__':
    pass
    # directory_path = './not_audio' 
    # features_df = process_directory(directory_path)
    # features_df.to_csv('not_songs.csv', index=False)