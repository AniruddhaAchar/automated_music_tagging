from Data_visualiztion import plot_confusion_matrix, plot_mfcc, plot_rmse, plot_spectral_bandwidth, \
    plot_spectral_centroid, plot_mfcc_histogram, plot_rmse_histogram

import matplotlib.pyplot as plt

from audio_feature_extraction import get_audio_features

'''from ML import getconfusion_matrix
from audio_feature_extraction import get_audio_features

svm = getconfusion_matrix('svm')
et = getconfusion_matrix('et')
rf = getconfusion_matrix('rf')
voting = getconfusion_matrix('vote')

plt.figure()
plot_confusion_matrix(svm, title='Confusion matrix, svm')
plt.figure()
plot_confusion_matrix(et, title='Confusion matrix, Extra Tree')
plt.figure()
plot_confusion_matrix(rf, title='Confusion matrix, Random Forest')
plt.figure()
plot_confusion_matrix(voting, title='Confusion matrix, voting')'''
#dinner_features = get_audio_features("E:\\final year project\\audio files\\dinner\\A Touch Of Silver.mp3")
#party_features = get_audio_features("E:\\final year project\\audio files\\party\\Aint My Fault.mp3")
sleep_features = get_audio_features("E:\\final year project\\audio files\\sleep\\A Sky Full of Flowers.mp3")
#workout_features = get_audio_features("E:\\final year project\\audio files\\workout\\A Milli.mp3")

#plot_mfcc(dinner_features['mfcc'],"Dinner")
#plot_mfcc(party_features['mfcc'],"Party")
#plot_mfcc(sleep_features['mfcc'],"Sleep")
#plot_mfcc(workout_features['mfcc'],"Workout")
#plt.figure()
#plot_mfcc_histogram([dinner_features['mfcc']],"Dinner")
#plt.figure()
#plot_mfcc_histogram([party_features['mfcc']],"Party")
plt.figure()
plot_mfcc_histogram([sleep_features['mfcc']],"Sleep")
#plt.figure()
#plot_mfcc_histogram([workout_features['mfcc']],"Workout")
plt.show()
