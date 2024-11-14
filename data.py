import os
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from pretrained import getGenre,getGenreMillion,getPopularity,getEngagement,getVA,getDanceability,getMoodGroup,getAggressive,getHappy,getRelaxed,getSad,getTimbre,getAcoustic,getElectronic,getGender,getInstrumental

# change this
is_hot = 0

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    try:
        # Extract MFCCs (Timbral Texture)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1) if mfccs.size > 0 else np.zeros(13)

        # Extract Chroma Features
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_stft_mean = np.mean(chroma_stft, axis=1) if chroma_stft.size > 0 else np.zeros(12)

        # Extract Spectral Features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

        spectral_centroid_mean = np.mean(spectral_centroid) if spectral_centroid.size > 0 else 0
        spectral_bandwidth_mean = np.mean(spectral_bandwidth) if spectral_bandwidth.size > 0 else 0
        spectral_contrast_mean = np.mean(spectral_contrast, axis=1) if spectral_contrast.size > 0 else np.zeros(7)
        spectral_rolloff_mean = np.mean(spectral_rolloff) if spectral_rolloff.size > 0 else 0


        # Extract BPM (Beats Per Minute)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Extract Zero Crossing Rate (Percussiveness)
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))

        # Extract Tonnetz (Tonal Space)
        tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
        tonnetz_mean = np.mean(tonnetz, axis=1) if tonnetz.size > 0 else np.zeros(6)
        
        # Extract from Essentia
        genre = getGenre(file_path)
        genrem = getGenreMillion(file_path)
        pop = getPopularity(file_path)
        eng = getEngagement(file_path)
        valence,arousal = getVA(file_path)
        dan, notdan = getDanceability(file_path)
        mgroup = getMoodGroup(file_path)
        agg,notagg = getAggressive(file_path)
        happy,nothappy = getHappy(file_path)
        relax,notrelax = getRelaxed(file_path)
        sad,notsad = getSad(file_path)
        bright,dark = getTimbre(file_path)
        acou,notacou = getAcoustic(file_path)
        elec,notelec = getElectronic(file_path)
        inst,vocal = getInstrumental(file_path)
        male,female = getGender(file_path)
        
        features = np.concatenate([
            [file_path.split('.mp3')[0].split('/')[-1]], [is_hot], [genre], [genrem], [pop], [eng], [valence], [arousal], [dan], [notdan], [mgroup],
            [agg], [notagg], [happy], [nothappy], [sad], [notsad], [relax], [notrelax], [bright], [dark], [acou], [notacou], [elec], [notelec], [inst],
            [vocal], [male], [female], mfccs_mean, chroma_stft_mean, [spectral_centroid_mean], [spectral_bandwidth_mean], spectral_contrast_mean,
            [spectral_rolloff_mean], tempo, [zero_crossing_rate], tonnetz_mean
        ])

        return features
    
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

def process_directory(directory_path):
    feature_list = []
    for file_name in tqdm(os.listdir(directory_path)):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(directory_path, file_name)
            features = extract_features(file_path)
            feature_list.append(features)
    
    # Create a DataFrame with the features
    column_names = [
        'name', 'is_hot', 'genre', 'style', 'popularity', 'engagement', 'valence', 'arousal', 'danceable', 'not_danceable',
        'mood_group', 'aggressive', 'not_aggressive', 'happy', 'not_happy', 'sad', 'not_sad', 'relaxing', 'not_relaxing',
        'bright', 'dark', 'acoustic', 'not_acoustic', 'electronic', 'not_electronic', 'instrumental', 'vocal', 'male', 'female',
        'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13',
        'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5', 'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11', 'chroma_12',
        'spectral_centroid', 'spectral_bandwidth', 'spectral_contrast_1', 'spectral_contrast_2', 'spectral_contrast_3', 'spectral_contrast_4', 'spectral_contrast_5', 'spectral_contrast_6', 'spectral_contrast_7',
        'spectral_rolloff', 'tempo', 'zero_crossing_rate',
        'tonnetz_1', 'tonnetz_2', 'tonnetz_3', 'tonnetz_4', 'tonnetz_5', 'tonnetz_6'
    ]
    features_df = pd.DataFrame(feature_list, columns=column_names)
    return features_df

if __name__ == '__main__':
    pass
    # directory_path = './not_audio' 
    # features_df = process_directory(directory_path)
    # features_df.to_csv('not_songs.csv', index=False)