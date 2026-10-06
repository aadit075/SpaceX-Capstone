"""Predict landing success with four classifiers."""
import os, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
B = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/"
data = pd.read_csv("dataset_part_2.csv" if os.path.exists("dataset_part_2.csv") else B + "dataset_part_2.csv")
X = pd.read_csv("features.csv" if os.path.exists("features.csv") else B + "dataset_part_3.csv")
Y = data["Class"].to_numpy()
X = StandardScaler().fit_transform(X)
Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.2, random_state=2)
models = {
 "Logistic Regression": (LogisticRegression(), {"C": [.01, .1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}),
 "SVM": (SVC(), {"kernel": ["linear", "rbf", "poly", "sigmoid"], "C": [.1, 1, 10], "gamma": ["scale"]}),
 "Decision Tree": (DecisionTreeClassifier(random_state=2), {"criterion": ["gini", "entropy"], "max_depth": [2*n for n in range(1, 10)],
                   "min_samples_leaf": [1, 2, 4], "min_samples_split": [2, 5, 10]}),
 "KNN": (KNeighborsClassifier(), {"n_neighbors": list(range(1, 11)), "p": [1, 2]})}
res, fitted = {}, {}
for n, (m, g) in models.items():
    gs = GridSearchCV(m, g, cv=10).fit(Xtr, Ytr)
    res[n] = gs.score(Xte, Yte); fitted[n] = gs
    print(f"{n}: cv={gs.best_score_:.4f} test={res[n]:.4f} params={gs.best_params_}")
best = max(res, key=res.get); print("Best model:", best)
cm = confusion_matrix(Yte, fitted[best].predict(Xte))
ConfusionMatrixDisplay(cm, display_labels=["did not land", "landed"]).plot(cmap="Blues")
plt.title(f"Confusion matrix - {best}"); plt.savefig("confusion_matrix.png", dpi=130)
