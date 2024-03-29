import json as js
import json as js
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

f = open('goemotions.json')
file = js.load(f)
split = np.array(file)
x = split[:, 0]
y1 = split[:, 1]
y2 = split[:, 2]

# Part 2.2
x1_train, x1_test, y1_train, y1_test = train_test_split(x, y1, train_size=0.8, test_size=0.2)
x2_train, x2_test, y2_train, y2_test = train_test_split(x, y2, train_size=0.8, test_size=0.2)

#PART 2.3.6 MLP
vec=CountVectorizer()


x1_train = vec.fit_transform(x1_train)
x1_test = vec.transform(x1_test)
#y1_train = vec.transform(y1_train)
y1_test = vec.transform(y1_test)

mlp = MLPClassifier(early_stopping=True, verbose=True, max_iter=1)
sc = StandardScaler(with_mean=False)
scaler_x = sc.fit(x1_train)
x1_train_scaled = scaler_x.transform(x1_train)
scaler_y = sc.fit(y1_train)
y1_train_scaled = scaler_y.transform(y1_train)

parameters= {
    'hidden_layer_sizes': ((5,5), (5,10)),
    'activation': ['logistic', 'tanh', 'relu', 'identity'],
    'solver': ['adam', 'sgd'],
    }
clf = GridSearchCV(estimator = mlp, param_grid=parameters, n_jobs=-1,error_score='raise')

clf.fit(x1_train_scaled, y1_train)
y1_pred= clf.predict(x1_test) 
print('accuracy: {:.2f}'.format(accuracy_score(y1_test, y1_pred)))
print("For emotions : \n")
print(classification_report(y1_test, y1_pred,zero_division=1))
print("Confusion Matrix: \n", confusion_matrix(y1_test, y1_pred))
x2_train = vec.fit_transform(x2_train)
x2_test = vec.transform(x2_test)
y2_train = vec.transform(y2_train)
y2_test = vec.transform(y2_test)
scaler_x2 = sc.fit(x2_train)
x2_train_scaled = scaler_x2.transform(x2_train)
scaler_y2 = sc.fit(y2_train)
y2_train_scaled = scaler_y2.transform(y2_train)

mlp1 = MLPClassifier(max_iter=1)
grid1=GridSearchCV(estimator=mlp1,param_grid=parameters,n_jobs=-1,error_score='raise')
grid1.fit(x2_train_scaled, y2_train)
y2_pred = grid1.predict(x2_test)
print("For sentiments : \n")
print(classification_report(y2_test, y2_pred, zero_division=1))
print("Confusion Matrix: \n", confusion_matrix(y2_test, y2_pred))
f.close()

