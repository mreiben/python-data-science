from sklearn import datasets
from sklearn.cross_validation import train_test_split, KFold
iris = datasets.load_iris()

import matplotlib.pyplot as plt

iris_train, iris_test = train_test_split(iris['data'], test_size=0.4, random_state=42)

print len(iris_train) #90
print len(iris_test) #60


kf = KFold(4, n_folds=2)
for train, test in kf:
    print("%s %s" % (train, test))
