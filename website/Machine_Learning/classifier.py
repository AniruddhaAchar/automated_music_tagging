from collections import Counter
from sklearn.externals import joblib
from config import ROOT_ML

activity_map = {1: "dinner", 2: "party", 3: "sleep", 4: "workout"}
# track machine learning algorithms
scaler_track = joblib.load(ROOT_ML + 'scaler_track.pkl')
svmclf_track = joblib.load(ROOT_ML + 'svm_Classifier_track.pkl')
etclf_track = joblib.load(ROOT_ML + 'extra_tree_classifier_track.pkl')
rfclf_track = joblib.load(ROOT_ML + 'random_forest_Classifier_track.pkl')

# audio machine learning algorithms
scaler_audio = joblib.load(ROOT_ML + 'scaler_audio.pkl')
svmclf_audio = joblib.load(ROOT_ML + 'svm_audio.pkl')
MLclf_audio = joblib.load(ROOT_ML + 'Neural_Network_audio.pkl')
Knnclf_audio = joblib.load(ROOT_ML + 'KNeighbors_audio.pkl')


def classify_track(audio_features):
    X = [audio_features['acousticness'], audio_features['danceability'], audio_features['energy'],
         audio_features['instrumentalness'], audio_features['speechiness'], audio_features['tempo'],
         audio_features['valence'], audio_features['loudness']]
    X = scaler_track.transform(X)
    X = X.reshape(1, -1)
    svmPred = svmclf_track.predict(X).tolist()[0]
    etPred = etclf_track.predict(X).tolist()[0]
    rfPred = rfclf_track.predict(X).tolist()[0]
    predictions = [svmPred, etPred, rfPred]
    votes = Counter(predictions)
    activity, count = votes.most_common()[0]
    return activity_map[activity]


def classify_audio(mfcc, scem, scom, srom, sbwm, tempo, rmse):
    X = [mfcc, scem, scom, srom, sbwm, tempo, rmse]
    X = scaler_audio.transform(X)
    X = X.reshape(1, -1)
    svmPred = svmclf_audio.predict(X).tolist()[0]
    NNPred = MLclf_audio.predict(X).tolist()[0]
    KnnPred = Knnclf_audio.predict(X).tolist()[0]
    predictions = [svmPred, NNPred, KnnPred]
    votes = Counter(predictions)
    activity, count = votes.most_common()[0]
    return activity_map[activity]
