from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
# import tensorflow as tf
# from tensorflow import Graph

# model_graph=Graph()
# with model_graph.as_default():
#   tf_session = tf.compat.v1.Session()
#   with tf_session.as_default():


def index(request):
  context= {'a':'this is a context from epl_webapp'}
  return render(request,'index.html',context)

def trial(request):
  context= {'a':'this is a trial page after submit'}
  if request.method == "POST":
    home=request.POST.get('home')
    away=request.POST.get('away')
    context= {'a':home,'b':away}

  return render(request,'test.html',context)

def predictor(request):
  if request.method == "POST":
    home=request.POST.get('home')
    away=request.POST.get('away')
    a=predict(home,away)
    context=a
    # context= {'home':home,'away':away,'out1':a["1"]}
  return render(request,'index.html',context)  


def single_predict(df,home,away):
  filtered_data = df[(df.HomeTeam == home) & (df.AwayTeam == away)]
  input_data= filtered_data[['HS','AS','HST','AST','HF','AF','HY','AY','HR','AR','HC','AC','HTR']]
  input_data.replace({"HTR":{'H':1,'A':2,'D':0}},inplace=True)
  _prediction=model.predict(input_data)
  Predicted=pd.DataFrame(_prediction)

  classes=pd.DataFrame(model.predict_classes(input_data))

  # classes=pd.DataFrame(_prediction)
  classes=classes.replace({0:{1:'H',2:'A',0:'D'}})
  Predicted['Predicted result']=classes[0]
  Predicted['HomeTeam']=home
  Predicted['AwayTeam']=away

  return Predicted


def predict(home,away):
  result=prediction[(prediction.HomeTeam == home) & (prediction.AwayTeam == away)]  #query in the dataframe (prediction)
  if int(result.shape[0]) > 0:
    index=result.index[0]
    FTR=result['FTR'][index]
    if (result['Predicted result'][index])=='H':
      winner="home"
  #     print("The predicted winner: ",home)
    else:
      winner="away"
  #     print("The predicted winner: ",away)
    output={'a':FTR,'b':winner}

  else:
  #   print("Prediction using data from previous matches")
    P = single_predict(old_data,home,away)
    winner=P['Predicted result'][0]
    # winner=P['HST'][0]

  #   print(P['Predicted result'][0])
  #   display(P)
    output={'a':"winner",'b':winner}
  # string="reached predict function"
  return output


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Path = os.path.join(BASE_DIR,"models","model.h5")
model = load_model(Path,compile=False)


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