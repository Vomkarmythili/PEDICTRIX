import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample dataset
data = {
    "temperature":[30,32,34,36,40,45,50,55],
    "vibration":[90,100,110,120,200,250,300,350],
    "status":[0,0,0,0,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[["temperature","vibration"]]
y = df["status"]

model = RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"model.pkl")

print("Model trained successfully")
