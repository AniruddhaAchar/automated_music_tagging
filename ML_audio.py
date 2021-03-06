from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from Database_connections import getAudioData
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import preprocessing
import numpy as np
from sklearn.neural_network import MLPClassifier


key_activity_map = {1: "dinner", 2: "party", 3: "sleep", 4: "workout"}
training_data_map = dict()
testing_data_map = dict()
for key in key_activity_map:
    training_data_map[key] = getAudioData(key_activity_map[key])
    testing_data_map[key] = getAudioData(key_activity_map[key],training=False)


X = []
Y = []
for key in training_data_map:
    temp = training_data_map[key]
    X.extend(temp)
    for ele in temp:
        Y.append(key)

scaler = preprocessing.StandardScaler().fit(X)
print(X)
X = scaler.transform(X)
Y = np.asarray(Y)

XTest = []
YTrue = []
for key in testing_data_map:
    temp = testing_data_map[key]
    XTest.extend(temp)
    for ele in temp:
        YTrue.append(key)

XTest = scaler.transform(XTest)

Knnclf = KNeighborsClassifier(n_neighbors=3)
Knnclf.fit(X, Y)

svmclf = SVC(C=1.55, decision_function_shape='ovr')
svmclf.fit(X, Y)

gnbclf = GaussianNB()
gnbclf.fit(X, Y)

rfclf = RandomForestClassifier(n_estimators=100, criterion="entropy", max_features='auto', random_state=1)
rfclf.fit(X, Y)

MLclf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(7,49), random_state=1, warm_start=True)
for i in range(5):
    MLclf.fit(X, Y)

etclf = ExtraTreesClassifier(criterion='entropy', n_estimators=100, max_features='auto')
etclf.fit(X, Y)


eclf = VotingClassifier(estimators=[('svm', svmclf), ('nn', MLclf), ('knn', Knnclf)], voting='hard')
eclf.fit(X, Y)

##joblib.dump(svmclf,"SVM_audio.pkl")
#joblib.dump(MLclf, 'Neural_Network_audio.pkl')
#joblib.dump(gnbclf,'GaussianNB_audio.pkl')
#joblib.dump(Knnclf, 'KNeighbors_audio.pkl')
#joblib.dump(scaler, 'scaler_audio.pkl')

KnnYPred = Knnclf.predict(XTest)
knnlist = KnnYPred.tolist()

svmYPred = svmclf.predict(XTest)
svmlist = svmYPred.tolist()

gnbclfYPred = gnbclf.predict(XTest)
gnblist = gnbclfYPred.tolist()

rfYpred = rfclf.predict(XTest)
rflist = rfYpred.tolist()

MLYpred = MLclf.predict(XTest)
MLYpred = MLYpred.tolist()

etYpred = etclf.predict(XTest)
etlist = etYpred.tolist()

votingPred = eclf.predict(XTest)
votingPred = votingPred.tolist()
print("kNN accuracy = {}% ".format(accuracy_score(YTrue, KnnYPred) * 100))
print("SVM accuracy = {}% ".format(accuracy_score(YTrue, svmYPred) * 100))
print("GNB accuracy = {}% ".format(accuracy_score(YTrue, gnbclfYPred) * 100))
print("RFaccuracy = {}% ".format(accuracy_score(YTrue, rfYpred) * 100))
print("NNaccuracy = {}%".format(accuracy_score(YTrue,MLYpred)*100))
print("ETaccuracy = {}% ".format(accuracy_score(YTrue, etYpred) * 100))
print("Voting accuracy = {}% ".format(accuracy_score(YTrue, votingPred) * 100))

def getconfusion_matrix(classifier):
    """

    :param classifier:
    :return: the confusion matrix of one of the classifiers or an error string
    """
    return {'svm': confusion_matrix(YTrue, svmYPred), 'NN': confusion_matrix(YTrue, MLYpred),
            'kNN': confusion_matrix(YTrue, KnnYPred), 'vote': confusion_matrix(YTrue, votingPred)}.get(classifier,
                                                                                                     "No classifier of that name")