from collections import Counter

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
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing
from sklearn.externals import joblib

from keras.models import Sequential
from keras.layers import Dense


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
'''
min_max_scaler = preprocessing.MinMaxScaler()
print(Y[-1])
scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)
print(X[-1])
Y = np.asarray(Y)
Knnclf = KNeighborsClassifier(n_neighbors=3)
Knnclf.fit(X, Y)
svmclf = SVC(C=2.015, gamma=0.005, decision_function_shape='ovo')
svmclf.fit(X, Y)
svmclf.decision_function(X)
gnbclf = GaussianNB()
gnbclf.fit(X, Y)
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
joblib.dump(svmclf, 'svm_Classifier_track.pkl')
joblib.dump(Knnclf, 'kNeighbors_Classifier_track.pkl')
joblib.dump(gnbclf, 'gaussian_NB_Classifier_track.pkl')
joblib.dump(rfclf, 'random_forest_Classifier_track.pkl')
joblib.dump(etclf, 'extra_tree_classifier_track.pkl')
joblib.dump(scaler, 'scaler_track.pkl')'''

XTest = []
YTrue = []
for key in testing_data_map:
    temp = testing_data_map[key]
    XTest.extend(temp)
    for ele in temp:
        YTrue.append(key)

'''XTest = scaler.transform(XTest)
KnnYPred = Knnclf.predict(XTest)
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
combinedYPred =[]
for s,e,r in zip(svmlist, etlist, rflist):
    predictions=[s,e,r]
    votes = Counter(predictions)
    activity, count = votes.most_common()[0]
    combinedYPred.append(activity)

print("kNN accuracy = {}% ".format(accuracy_score(YTrue, KnnYPred) * 100))
print("SVM accuracy = {}% ".format(accuracy_score(YTrue, svmYPred) * 100))
print("GNB accuracy = {}% ".format(accuracy_score(YTrue, gnbclfYPred) * 100))
print("DT accuracy = {}% ".format(accuracy_score(YTrue, dtYPred) * 100))
print("RFaccuracy = {}% ".format(accuracy_score(YTrue, rfYpred) * 100))
print("ETaccuracy = {}% ".format(accuracy_score(YTrue, etYpred) * 100))
print("GBaccuracy = {}% ".format(accuracy_score(YTrue, gbYpred) * 100))
print("MCaccuracy = {}% ".format(accuracy_score(YTrue, mplclf) * 100))
print("NNaccuracy = {}%".format(accuracy_score(YTrue,MLYpred)*100))
print("NNaccuracy = {}%".format(accuracy_score(YTrue,MLYpred)*100))
'''
# create model
model = Sequential()
model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=150, batch_size=10)
# evaluate the model
scores = model.evaluate(X, Y)
#print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
classes = model.predict_classes(XTest, batch_size=32)
loss_and_metrics = model.evaluate(XTest, YTrue, batch_size=32)
print("Loss and metrics"+loss_and_metrics)
print("Classes"+classes)