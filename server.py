########## SECTION OF Import Libary ##########

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt #Import for Test#
import random #Import for Test#
from sklearn.metrics import accuracy_score
import requests
from datetime import datetime

########## END OF Import Libary ##########

########## SECTION OF PREDICTOR MODEL ##########

# Read data
data=pd.read_csv('DataFake1_tree.csv')

data.head()

X = data.iloc[:, [ 1, 2, 3, 4]].values
y = data.iloc[:, 5].values

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=22)
#X_train, X_test, y_train, y_test = X, X, y, y

# Create model object
clf = MLPClassifier(hidden_layer_sizes=(100), 
                    max_iter=300,
                    activation = 'logistic',
                    solver='adam',
                    random_state=1)

# Fit data onto the model
history = clf.fit(X_train,y_train)

# plt.plot(clf.loss_curve_)
# plt.title("Loss Curve", fontsize=14)
# plt.xlabel('Iterations')
# plt.ylabel('Cost')
# plt.show()

# Make prediction on test dataset
ypred = clf.predict(X_test)

# Calcuate accuracy
accuracy_score(y_test,ypred)

########## END OF SECTION PREDICTOR MODEL ##########


########## SECTION OF WeatherCheck ##########
#WEB SERVICE https://openweathermap.org/api
#https://www.aipython.in/python-project-weather-info-via-api/

user_api = "7b9a86d2006cc3e7c4c1c2d4bc38d743"

### ZIPCODE FOR SELECT LOCATION ###
Zipcode = "20000"

# https://api.openweathermap.org/data/2.5/weather?zip=94040,us&appid={API key}
complete_api_link = "https://api.openweathermap.org/data/2.5/weather?zip="+Zipcode+",th&appid="+user_api
api_link = requests.get(complete_api_link)
api_data = api_link.json()

#create variables to store and display data
temp_city = ((api_data['main']['temp']) - 273.15)
weather_desc = api_data['weather'][0]['description']
hmdt = api_data['main']['humidity']
wind_spd = api_data['wind']['speed']
date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
location = api_data['name']

# print ("-------------------------------------------------------------")
# print ("Weather Stats for - {}  || {}".format(location.upper(), date_time))
# print ("-------------------------------------------------------------")

# print ("Current temperature is: {:.2f} deg C".format(temp_city))
# print ("Current weather desc  :",weather_desc)
# print ("Current Humidity      :",hmdt, '%')
# print ("Current wind speed    :",wind_spd ,'kmph')

########## END OF SECTION WeatherCheck ##########

########## SECTION OF PREDICTOR ##########

def prediction(A, weather_desc, temp_city, B):
  print(weather_desc)
  if weather_desc.find("rain"):
    weather_desc = 1
  else:
    weather_desc = 0
  inpredict = [[A,weather_desc,temp_city,B]]
  opredict = clf.predict(inpredict)
  print(inpredict)
  print(opredict)


  return opredict

########## END OF SECTION PREDICTOR ##########

prediction(random.randrange(50,80), weather_desc, temp_city, random.randrange(0,100))