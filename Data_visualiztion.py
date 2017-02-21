import itertools

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def plot_confusion_matrix(cm, classes=["dinner", "party", "sleep", "workout"], title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def plot_mfcc(mfcc, title=""):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc, x_axis='time')
    plt.colorbar()
    plt.title('MFCC of ' + title)
    plt.tight_layout()

def plot_mfcc_histogram(mfcc, title):
    if title == 'all':
        plt.hist(mfcc,bins=50, log=True, stacked=True, label=['party', 'dinner', 'sleep', 'workout'], alpha=0.5)
    else:
        plt.hist(mfcc, bins=50, log=True, alpha=0.5)
    plt.title("MFCC Histogram "+title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

def plot_rmse_histogram(rmse, title):
    if title == 'all':
        plt.hist(rmse, bins=50, log=True, stacked=True, label=['party', 'dinner', 'sleep', 'workout'], alpha=0.5)
    else:
        plt.hist(rmse, bins=50, log=True, alpha=0.5)
    plt.title("RMSE Histogram "+title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

def plot_rmse(rmse, S, title=""):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.semilogy(rmse.T, label='RMS Energy')
    plt.xticks([])
    plt.xlim([0, rmse.shape[-1]])
    plt.legend(loc='best')
    plt.subplot(2, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')
    plt.title('log Power spectrogram of ' + title)
    plt.tight_layout()


def plot_spectral_centroid(cent, S, title=""):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.semilogy(cent.T, label='Spectral centroid')
    plt.ylabel('Hz')
    plt.xticks([])
    plt.xlim([0, cent.shape[-1]])
    plt.legend()
    plt.subplot(2, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                             y_axis='log', x_axis='time')
    plt.title('log Power spectrogram of ' + title)
    plt.tight_layout()


def plot_spectral_bandwidth(spec_bw, S, title=""):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.semilogy(spec_bw.T, label='Spectral bandwidth')
    plt.ylabel('Hz')
    plt.xticks([])
    plt.xlim([0, spec_bw.shape[-1]])
    plt.legend()
    plt.subplot(2, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                             y_axis='log', x_axis='time')
    plt.title('log Power spectrogram')
    plt.tight_layout()
