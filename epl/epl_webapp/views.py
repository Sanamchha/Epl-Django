from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

model = joblib.load('./models/model.h5')


def index(request):
	context= {'a':'this is a context from epl_webapp'}
	return render(request,'test.html',context)


def predictor(request):
	if request.method == "POST":
		home=request.POST.get('home')
		away=request.POST.get('away')
		predictor(home,away)
		context= {'home':home,'away':away}
	return render(request,'test.html',context)	


def single_predict(df,home,away):
  filtered_data = df[(df.HomeTeam == home) & (df.AwayTeam == away)]
  input_data= filtered_data[['HS','AS','HST','AST','HF','AF','HY','AY','HR','AR','HC','AC','HTR']]
  input_data.replace({"HTR":{'H':1,'A':2,'D':0}},inplace=True) 
  Predicted=pd.DataFrame(model.predict(input_data))
  classes=pd.DataFrame(model.predict_classes(input_data))
  classes=classes.replace({0:{1:'H',2:'A',0:'D'}})
  Predicted['Predicted result']=classes[0]
  Predicted['HomeTeam']=home
  Predicted['AwayTeam']=away

  return Predicted


def predictor(home,away):
  result=prediction[(prediction.HomeTeam == home) & (prediction.AwayTeam == away)]  #query in the dataframe (prediction) 
  if int(result.shape[0]) > 0:
    index=result.index[0]
    print("The actual FTR is ",(result['FTR'][index]))
    if (result['Predicted result'][index])=='H':
      print("The predicted winner: ",home)
    else:
      print("The predicted winner: ",away)
  else:
    print("Prediction using data from previous matches")
    P = single_predict(old_data,home,away)
    print(P['Predicted result'][0])
    display(P)



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
r_path = os.path.join(BASE_DIR,"data","recent.csv")
t_path = os.path.join(BASE_DIR,"data","tester.csv")
old_data = pd.read_csv(r_path)
tester = pd.read_csv(t_path)
pred_data = tester[['HS','AS','HST','AST','HF','AF','HY','AY','HR','AR','HC','AC','HTR']]

scaler = MinMaxScaler()
pred_data.replace({"HTR":{'H':1,'A':2,'D':0}},inplace=True)
pred_data = scaler.fit_transform(pred_data)

result=model.predict(pred_data)
Class_prediction=pd.DataFrame(model.predict_classes(pred_data))
Class_prediction.replace({0:{1:'H',2:'A',0:'D'}},inplace=True)

prediction = tester[['HomeTeam','AwayTeam','FTR']]
result=pd.DataFrame(result)
prediction['Draw']=result[[0]]
prediction['Homewin']=result[[1]]
prediction['awaywin']=result[[2]]
prediction['Predicted result']=Class_prediction

#here prediction <type 'Dataframe'> has the predicted result