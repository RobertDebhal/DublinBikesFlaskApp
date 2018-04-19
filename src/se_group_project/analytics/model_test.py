import pickle
import pandas as pd

with open("./10/4/6/model.pkl","rb") as input:
	model = pickle.load(input)
	
def predict(model):
	df = pd.DataFrame([[1,1,1,0]], columns=['wind','temperature','rain_True','rain_False'])
	print(model.predict(df))

predict(model)