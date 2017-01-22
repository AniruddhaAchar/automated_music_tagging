import librosa
import numpy as np

from Machine_Learning import classifier
from config import UPLOAD_FOLDER


def get_audio_features(file_name):
    file_path = UPLOAD_FOLDER + "\\" + file_name
    print(file_path)
    y, sr = librosa.load(file_path)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    if_gram, D = librosa.ifgram(y)
    S = np.abs(librosa.stft(y))
    mag_SC = librosa.feature.spectral_centroid(S=np.abs(D), freq=if_gram)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    rmse = librosa.feature.rmse(y=y)
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.estimate_tempo(onset_env, sr=sr)
    activity = classifier.classify_audio(scem=spectral_centroid.mean(), scom=contrast.mean(),
                              mfcc=mfcc.mean(), rmse=rmse.mean(), sbwm=spectral_bandwidth.mean(),
                              srom=spectral_rolloff.mean(),
                              tempo=tempo)
    return activity
