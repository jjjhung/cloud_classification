from sklearn import svm

import numpy as np 
import helpers
import eaeri as er

X = helpers.read_obj('features')
y = helpers.read_obj('tags')

X = np.array(X)
y = np.array(y)

print(np.shape(X))
eaeri_dataframes = helpers.read_eaeri(["2008"])

eaeri = {}
for days in eaeri_dataframes:
    print(days)
    eaeri[days] = er.EAERI(eaeri_dataframes[days])

# -------------------- LOAD DATA HERE ---------------------
# n: number of data samples
# m: number of features
# X = data, matrix of size (n,m)
# y = target vectors, vector of size (n,1)

# Samples to be evaluated should be of size (m,1)
svc = svm.SVC(kernel='rbf', gamma = 0.7, C=1.0).fit(X,y) # This trains a SVM classifier with rbf kernel

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