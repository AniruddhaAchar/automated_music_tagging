from Data_visualiztion import plot_confusion_matrix, plot_mfcc, plot_rmse, plot_spectral_bandwidth, \
    plot_spectral_centroid
from ML import getconfusion_matrix
import matplotlib.pyplot as plt

from audio_feature_extraction import get_audio_features

svm = getconfusion_matrix('svm')
rf = getconfusion_matrix('rf')
et = getconfusion_matrix('et')
voting = getconfusion_matrix('vote')

plt.figure()
plot_confusion_matrix(svm, title='Confusion matrix, svm')
plt.figure()
plot_confusion_matrix(rf, title='Confusion matrix, rf')
plt.figure()
plot_confusion_matrix(et, title='Confusion matrix, et')
plt.figure()
plot_confusion_matrix(voting, title='Confusion matrix, voting')

audio_features = get_audio_features("F:\music\party\\Avicii - Levels.mp3")
title = "Avicii - Levels"
plot_mfcc(audio_features['mfcc'], title=title)
plot_rmse(audio_features['rsme'], audio_features['S'], title=title)
plot_spectral_bandwidth(audio_features['spectral_bandwidth'], audio_features['S'], title=title)
plot_spectral_centroid(audio_features['spectral_centroid'], audio_features['S'], title=title)
plt.show()
