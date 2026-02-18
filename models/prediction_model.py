import pandas as pd
from sklearn.linear_model import LogisticRegression

# train model once
data = pd.read_csv("dataset/students.csv")

X = data[["avg_marks", "dsa", "projects", "aptitude"]]
y = data["placed"]

model = LogisticRegression()
model.fit(X, y)

def predict_placement(avg_marks, dsa, projects, aptitude):
    prob = model.predict_proba([[avg_marks, dsa, projects, aptitude]])[0][1]
    return round(prob * 100, 2)
