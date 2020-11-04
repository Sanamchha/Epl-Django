from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	context= {'a':'this is a context from epl_webapp'}
	return render(request,'test.html',context)


def predictor(request):
	if request.method == "POST":
		print("request is post")
		print(request.POST.get('home'))
	context= {'a':'after submission'}
	return render(request,'test.html',context)	

