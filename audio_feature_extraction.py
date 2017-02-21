from os import listdir
import librosa
import numpy as np
from Database_connections import addAudioFeatures, Create_table

file_name = None


def extractMusicFeatures(file_name, file_details):
    y, sr = librosa.load(file_name)
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
    zero_crossing = librosa.feature.zero_crossing_rate(y)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.estimate_tempo(onset_env, sr=sr)
    print("File: ", file_details)
    print("Chroma", chroma.mean(1))
    print("MSG_SC", mag_SC.mean())
    print("MFCC", mfcc.mean())
    print("Spectral Contrast mean", contrast.mean())
    print("Spectral roll off mean", spectral_rolloff.mean())
    print("Spectral centroid mean", spectral_centroid.mean())
    print("Spectral bandwidth mean", spectral_bandwidth.mean())
    print("Tempo", tempo)
    print("RSME", rmse)

    Create_table("workout")
    addAudioFeatures(name=file_details, database="workout", scem=spectral_centroid.mean(), scom=contrast.mean(),
                     mfcc=mfcc.mean(), rmse=rmse.mean(), sbwm=spectral_bandwidth.mean(), srom=spectral_rolloff.mean(),
                     tempo=tempo)


def get_audio_features(file_path):
    """
    computes various temporal and timber features related to the song
    :param file_path:
    :return: an dict() of the computed values.
    """
    print("Audio feature extraction started")
    y, sr = librosa.load(file_path)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    S = np.abs(librosa.stft(y))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    rmse = librosa.feature.rmse(y=y)
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(y)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.estimate_tempo(onset_env, sr=sr)
    return {"mfcc": mfcc, "rmse": rmse, "spectral_centroid": spectral_centroid,
            "spectral_bandwidth": spectral_bandwidth, "spectral_rolloff": spectral_rolloff,
            "zero_crossing": zero_crossing, "tempo": tempo, "S":S}

def get_training_data():
    for file in listdir("E:\\final year project\\audio files\\workout"):
        file_URL = "E:\\final year project\\audio files\\workout\\" + file
        extractMusicFeatures(file_URL, file)
