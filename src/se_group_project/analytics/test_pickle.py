import pickle
import pandas as pd


def predict_coefficients(modelled_data):
	return modelled_data.coef_

def predict_intercept(modelled_data):
	return modelled_data.intercept_

if __name__=='__main__':
	station = input('Enter station: ')
	day = input('Enter day: ')
	hour = input('Enter hour: ')
	with open('./'+station+'/'+day+'/'+hour+'/model.pkl','rb') as f:
		data = pickle.load(f)
	inter= predict_coefficients(data)
	coef = predict_intercept(data)
	print('Intercept: ',inter,'\ncoef :',coef )
	test_df = pd.DataFrame([[10,10,1,0]],columns = ['wind','temperature','rain_True','rain_False'])
	print('Intercept: ',inter,'\ncoef :',coef )
	