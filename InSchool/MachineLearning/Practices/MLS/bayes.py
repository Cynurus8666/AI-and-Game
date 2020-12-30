from __future__ import print_function
from sklearn.naive_bayes import MultinomialNB
import numpy as np

d1 = [2, 1, 1, 0, 0, 0, 0, 0, 0]
d2 = [1, 1, 0, 1, 1, 0, 0, 0, 0]
d3 = [0, 1, 0, 0, 1, 1, 0, 0, 0]
d4 = [0, 1, 0, 0, 0, 0, 1, 1, 1]

train_data = np.array([d1, d2, d3, d4])
label = np.array(['B', 'B', 'B', 'N'])

d5 = np.array([[2, 0, 0, 1, 0, 0, 0, 1, 0]])
d6 = np.array([[0, 1, 0, 0, 0, 0, 0, 1, 1]])
d7 = np.array([[1, 1, 1, 0, 0, 0, 0, 1, 1]])
d8 = np.array([[3, 1, 0, 0, 0, 0, 0, 2, 1]])


clf = MultinomialNB()
clf.fit(train_data, label)


print('Predicting class of d8: ', str(clf.predict(d8)))
print('Probability of d8 in each class: ', clf.predict_proba(d8))
