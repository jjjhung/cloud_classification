from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler

import numpy as np 
import helpers
import eaeri as er

X = helpers.read_obj('features')
y = helpers.read_obj('tags')

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=2)
#print(np.shape(X))

#Normalize input features
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

lda = LDA(n_components=10)
X_train = lda.fit_transform(X_train, y_train)
X_test = lda.transform(X_test)


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

correct = 0
for i, sample in enumerate(X_test):
    sample = sample.reshape(1,np.shape(sample)[0])
    predicted = svc.predict(sample)[0]
    if predicted == '0' or predicted == '1':
        if y_test[i] == '0' or y_test[i] == '1':
            correct += 1
    elif predicted == '2':
        if y_test[i] == '2':
            correct += 1 

print("Accuracy is at " + str(correct/len(X_test)) + " %")

while True:
    inp = input("Enter a time to classify clouds (e to exit): ")

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
    print(np.shape(input_features))
    print(svc.predict(input_features))