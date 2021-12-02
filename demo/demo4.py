import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from scipy.special import expit
plt.style.use('seaborn')

y = []
X = np.random.uniform(-3, 3, size=(20,1))
for i in X:
    if i > 0:
        y.append(1)
    else:
        y.append(0)

clf = LogisticRegression(C=1e5)
clf.fit(X, y)

plt.figure(1, figsize=(4, 3))
plt.clf()
plt.scatter(X.ravel(), y, c=['orange' if l == 1 else 'green' for l in y], zorder=10)
X_test = np.linspace(-5, 10, 1000)

curve = expit(X_test * clf.coef_ + clf.intercept_).ravel()
plt.plot(X_test, curve, color="red")


plt.ylabel("y")
plt.xlabel("x")
plt.yticks([0, 0.5, 1])
plt.ylim(-0.25, 1.25)
plt.xlim(-3, 3)
plt.tight_layout()
plt.savefig("logistic_regression.png")