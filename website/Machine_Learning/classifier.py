from collections import Counter
from sklearn import preprocessing
from sklearn.externals import joblib
from config import ROOT_ML

activity_map = {1: "dinner", 2: "party", 3: "sleep", 4: "workout"}
scaler = joblib.load(ROOT_ML + 'scaler_track.pkl')
svmclf = joblib.load(ROOT_ML + 'svm_Classifier_track.pkl')
etclf = joblib.load(ROOT_ML + 'extra_tree_classifier_track.pkl')
rfclf = joblib.load(ROOT_ML + 'random_forest_Classifier_track.pkl')


def classify_track(audio_features):
    X = [audio_features['acousticness'], audio_features['danceability'], audio_features['energy'],
         audio_features['instrumentalness'], audio_features['speechiness'], audio_features['tempo'],
         audio_features['valence'], audio_features['loudness']]
    X = scaler.transform(X)
    X = X.reshape(1, -1)
    svmPred = svmclf.predict(X).tolist()[0]
    etPred = etclf.predict(X).tolist()[0]
    rfPred = rfclf.predict(X).tolist()[0]
    predictions = [svmPred, etPred, rfPred]
    votes = Counter(predictions)
    activity, count = votes.most_common()[0]
    return activity_map[activity]

def classify_audio(mfcc, scem, scom, srom, sbwm, tempo, rmse):
