from sklearn.neural_network import MLPClassifier

from Database_connections import getData, getTestData
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing
from sklearn.externals import joblib

key_activity_map = {1: "dinner", 2: "party", 3: "sleep", 4: "workout"}
training_data_map = dict()
testing_data_map = dict()
for key in key_activity_map:
    training_data_map[key] = getData(key_activity_map[key])
    testing_data_map[key] = getTestData(key_activity_map[key])

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

'''Knnclf = KNeighborsClassifier(n_neighbors=3)
Knnclf.fit(X, Y)
svmclf = SVC(C=2.015, gamma=0.005, decision_function_shape='ovo')
svmclf.fit(X, Y)
svmclf.decision_function(X)
gnbclf = GaussianNB()
gnbclf.fit(X, Y)'''
knnclf = joblib.load('knnClassifier.pkl')
svmclf = joblib.load('svmClassifier.pkl')
gnbclf = joblib.load('gnbClassifier.pkl')
dtclf = tree.DecisionTreeClassifier(criterion='entropy')
dtclf.fit(X, Y)
rfclf = RandomForestClassifier(n_estimators=100, criterion="entropy", max_features='auto', random_state=1)
rfclf.fit(X, Y)
etclf = ExtraTreesClassifier(criterion='entropy', n_estimators=100, max_features='auto')
etclf.fit(X, Y)
gbclf = GradientBoostingClassifier(criterion='mse', max_features='auto', min_samples_split=3)
gbclf.fit(X, Y)
MLclf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                      hidden_layer_sizes=(5, 25), random_state=1, warm_start=True)
for i in range(10):
    MLclf.fit(X, Y)
'''joblib.dump(svmclf, 'svmClassifier.pkl')
joblib.dump(Knnclf, 'knnClassifier.pkl')
joblib.dump(gnbclf, 'gnbClassifier.pkl')'''

XTest = []
YTrue = []
for key in testing_data_map:
    temp = testing_data_map[key]
    XTest.extend(temp)
    for ele in temp:
        YTrue.append(key)

XTest = preprocessing.scale(XTest)

KnnYPred = knnclf.predict(XTest)
knnlist = KnnYPred.tolist()

svmYPred = svmclf.predict(XTest)
svmlist = svmYPred.tolist()
gnbclfYPred = gnbclf.predict(XTest)
gnblist = gnbclfYPred.tolist()
dtYPred = dtclf.predict(XTest)
dtlist = dtYPred.tolist()
rfYpred = rfclf.predict(XTest)
rflist = rfYpred.tolist()
etYpred = etclf.predict(XTest)
etlist = etYpred.tolist()
gbYpred = gbclf.predict(XTest)
gblist = gbYpred.tolist()
classif = OneVsRestClassifier(estimator=SVC(C=2.5, gamma=0.005))
classif.fit(X, Y)
mplclf = classif.predict(XTest)
MLYpred = MLclf.predict(XTest)
MLYpred = MLYpred.tolist()
print("kNN accuracy = {}% ".format(accuracy_score(YTrue, KnnYPred) * 100))
print("SVM accuracy = {}% ".format(accuracy_score(YTrue, svmYPred) * 100))
print("GNB accuracy = {}% ".format(accuracy_score(YTrue, gnbclfYPred) * 100))
print("DT accuracy = {}% ".format(accuracy_score(YTrue, dtYPred) * 100))
print("RFaccuracy = {}% ".format(accuracy_score(YTrue, rfYpred) * 100))
print("ETaccuracy = {}% ".format(accuracy_score(YTrue, etYpred) * 100))
print("GBaccuracy = {}% ".format(accuracy_score(YTrue, gbYpred) * 100))
print("MCaccuracy = {}% ".format(accuracy_score(YTrue, mplclf) * 100))
print("NNaccuracy = {}%".format(accuracy_score(YTrue,MLYpred)*100))
