# define a function call that takes in a mp3 file and return the 
# a. analysis json file
# b. Banger: True or False

# brew install libomp
import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from data import extract_features

def infer(file_path):
    # Load the trained models
    cat = joblib.load('./models/cat.pkl')
    xgb_model = joblib.load('./models/xgb.pkl')
    # rf = joblib.load('rf.pkl')

    # Load the dataset to ensure consistent encoding
    full_data = pd.read_csv('hot_or_not.csv')

    # Extract features from the new audio file
    features = extract_features(file_path)
    feature_list = [features]  # Wrap features in a list to create a DataFrame

    # Create a DataFrame for the new audio's features
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
    
    # Save Analysis File
    df_new_audio = pd.DataFrame(feature_list, columns=column_names)
    df_new_audio.to_csv(f"./analysis_files/{file_path.split('/')[-1]}.csv",index=False)
    
    # Drop unnecessary columns from the new audio DataFrame
    df_new_audio = df_new_audio.drop(['name', 'is_hot', 'not_danceable', 'not_aggressive', 'not_happy', 'not_sad',
                                      'not_relaxing', 'not_acoustic', 'not_electronic', 'male', 'instrumental', 'dark'], axis=1)
    
    # Insert the new audio's features at the top of the full dataset
    full_data = full_data.drop(['name', 'is_hot', 'not_danceable', 'not_aggressive', 'not_happy', 'not_sad',
                                'not_relaxing', 'not_acoustic', 'not_electronic', 'male', 'instrumental', 'dark'], axis=1)
    full_data.loc[-1] = df_new_audio.loc[0]  # Insert new data at index 0
    full_data.index = full_data.index + 1  # Shift the index
    full_data = full_data.sort_index()  # Sort by index to ensure the new entry is at the top

    # Prepare for CatBoost predictions
    cat_features = ['genre', 'style', 'mood_group']
    pool = Pool(full_data.iloc[[0]], cat_features=cat_features)
    y_pred_cat = cat.predict(pool)
    
    print(y_pred_cat)

    # Ensure the full dataset is consistently encoded
    full_data_encoded = pd.get_dummies(full_data, columns=['genre', 'style', 'mood_group'])
    full_data_encoded = full_data_encoded.apply(pd.to_numeric, errors='coerce')
    
    # Extract only the newly added entry (which is now at index 0) for prediction
    df_encoded = full_data_encoded.iloc[[0]]  # Select the first row for prediction
    
    # Predict with RandomForest and XGBoost
    y_pred_xgb = xgb_model.predict(df_encoded)
    print(y_pred_xgb)
    
    # y_pred_rf = rf.predict(df_encoded)
    # print(y_pred_rf)
    
    # Final decision: if any model predicts '1', return True
    if 1 in y_pred_cat or 1 in y_pred_xgb:
        print(True)
        return True
    else:
        print(False)
        return False

if __name__ == '__main__':
    # infer('./uploads/maye.mp3')
    pass