from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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

min_max_scaler = preprocessing.MinMaxScaler()
X = preprocessing.scale(X)
Y = np.asarray(Y)

XTest = []
YTrue = []
for key in testing_data_map:
    temp = testing_data_map[key]
    XTest.extend(temp)
    for ele in temp:
        YTrue.append(key)

XTest = preprocessing.scale(XTest)

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
for i in range(10):
    MLclf.fit(X, Y)



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

print("kNN accuracy = {}% ".format(accuracy_score(YTrue, KnnYPred) * 100))
print("SVM accuracy = {}% ".format(accuracy_score(YTrue, svmYPred) * 100))
print("GNB accuracy = {}% ".format(accuracy_score(YTrue, gnbclfYPred) * 100))
print("RFaccuracy = {}% ".format(accuracy_score(YTrue, rfYpred) * 100))
print("NNaccuracy = {}%".format(accuracy_score(YTrue,MLYpred)*100))