from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

import numpy as np 
import helpers
import eaeri as er

X = helpers.read_obj('features_2')
y = helpers.read_obj('tags_2')

X = np.array(X)[:326]
#X = np.append(np.array(X)[:326], np.array(X)[400:], axis=0)
y = np.array(y)[:326]
#y = np.append(np.array(y)[:326], np.array(y)[400:], axis=0)
print(np.shape(X))
#X=np.array(X)
#y=np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=2)
#print(np.shape(X))

#Normalize input features
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

lda = LDA(n_components=10)
X_train = lda.fit_transform(X_train, y_train)
X_test = lda.transform(X_test)

print(X_train)
print(X_test)

eaeri_dataframes = helpers.read_eaeri(["2008"])

eaeri = {}
for days in eaeri_dataframes:
    #print(days)
    eaeri[days] = er.EAERI(eaeri_dataframes[days])

# -------------------- LOAD DATA HERE ---------------------
# n: number of data samples
# m: number of features
# X = data, matrix of size (n,m)
# y = target vectors, vector of size (n,1)

# Samples to be evaluated should be of size (m,1)
svc = svm.SVC(kernel='rbf', gamma = 0.7, C=1.0).fit(X_train,y_train) # This trains a SVM classifier with rbf kernel
mlp = MLPClassifier(solver='adam', alpha=1e-3, hidden_layer_sizes=(1000,300), random_state=4, batch_size='auto').fit(X_train,y_train)

correct_svc = 0
correct_mlp = 0
for i, sample in enumerate(X_test):
    sample = sample.reshape(1,np.shape(sample)[0])
    print(sample)
    print(np.shape(sample))
    predicted_svc = svc.predict(sample)[0]
    predicted_mlp = mlp.predict(sample)[0]
#    print(predicted_svc)
#    print(y_test[i]) 
    if str(predicted_svc) == '0' or str(predicted_svc) == '1':
        if str(y_test[i]) == '0' or str(y_test[i]) == '1':
            correct_svc += 1
    elif str(predicted_svc) == '2':
        if str(y_test[i]) == '2':
            correct_svc += 1 

    if str(predicted_mlp) == '0' or str(predicted_mlp) == '1':
        if str(y_test[i]) == '0' or str(y_test[i]) == '1':
            correct_mlp += 1
    elif str(predicted_mlp) == '2':
        if str(y_test[i]) == '2':
            correct_mlp += 1 

print("SVM Accuracy is at " + str(correct_svc/len(X_test)) + " %")
print("MLP Accuracy is at " + str(correct_mlp/len(X_test)) + " %")

while True:
    inp = input("Enter a time to classify clouds (e to exit) [YYYY:MM:DD HH:MM:SS: ")

    if input == "e":
        break

    date = inp[2:4] + inp[5:7] + inp[8:10]

    print(date)

    try:
        time = eaeri[date].find_closest_spectra(inp)
    except KeyError:
        print("No spectra recorded for specified date")
        continue

    print("The closest recorded spectra is " + str(time))

    BT_features = eaeri[date].retrieve_microwindow_averages(time)
    extracted_features = er.EAERI.retrieve_microwindow_differences(BT_features)

    input_features = np.array(extracted_features)[:,1].reshape(1,91)
    input_features = lda.transform(input_features)
    print(np.shape(input_features))
    
    print("SVM Prediction", str(svc.predict(input_features)))
    print("MLP Prediction", str(mlp.predict(input_features)))


