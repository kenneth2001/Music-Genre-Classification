import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
import graphviz

x = np.random.uniform(-10, 10, size=(500, 2))
y = []

for i in x:
    if i[0] > 0:
        if i[1] > 0:
            y.append(0)
        else:
            y.append(1)
    else:
        y.append(2)

clf = DecisionTreeClassifier(max_depth=5)
clf.fit(x, y)

dot_data = tree.export_graphviz(
    clf, filled=True, label='all', class_names=['0', '1', '2'])
graph = graphviz.Source(dot_data, format="png")
graph.render("decision_tree")
