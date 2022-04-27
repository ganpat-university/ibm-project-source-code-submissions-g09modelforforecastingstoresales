from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
import csv, io
from rest_framework import views
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files import File
from datetime import datetime
from django.views import generic


import json
import urllib
from django.conf import settings

from . import models
from .models import ForecastModel
from django.views.generic import TemplateView

from .models import ForecastModel
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index1(request):
    user_list = models.ForecastModel.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user_list.html', { 'users': users })

# prediction
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split 
from sklearn.metrics import r2_score 

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('/upload')
    else:
        return render(request, 'index.html')

def mg(request):
    return render(request, 'graph.html')

# def graph(request):
    # return render(request,'graph.html',{'item':ForecastModel.objects.filter(Year_of_Release='2006').aggregate(Sum('Global_Sale'))})

class GIClinicStateCount(views.APIView):
    template_name = 'graph.html'

    def get(self,request,name=None):
        # importing the csv module
        import csv
            
            
        # name of csv file      

        gicliniclist = models.ForecastModel.objects.filter()[0]
        count= 0
        Save_arr = []
        arr = []
        allyear = models.ForecastModel.objects.values_list('Year_of_Release', flat=True).order_by('Year_of_Release').distinct()
        for year in allyear:
            count = models.ForecastModel.objects.filter(Year_of_Release=year).values('Global_Sale','Year_of_Release').distinct().aggregate(Sum('Global_Sale'))
            # print('countGIClinicStateCount',count)
            # skip 2 year 
            if year == '2020'or year == '2017':
                pass
            else:
                arr.append({"year":year,"count":count})
                Save_arr.append({"year":year,"count":count['Global_Sale__sum']})
        # field names
        fields = ['year', 'count']

        filename = "university_records.csv"
            
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames = fields)
                
            # writing headers (field names)
            writer.writeheader()
                
            # writing data rows
            writer.writerows(Save_arr)

        return render(request,'graph.html',{
        'labels': count,
        'data': arr,})

class GraphGenre(views.APIView):
    template_name = 'graphGenre.html'

    def get(self,request,Selectyear=None):
        print('selectYear',Selectyear)
        gicliniclist = models.ForecastModel.objects.filter()[0]
        count= 0
        arr = []
        yearArr = []
        # allyear = models.ForecastModel.objects.values_list('Year_of_Release', flat=True).order_by('Year_of_Release').distinct()
        allyear = models.ForecastModel.objects.values_list('Year_of_Release','Genre').order_by('Genre').distinct()
        allgenre = models.ForecastModel.objects.values_list('Genre').distinct()

        selectYear = models.ForecastModel.objects.values_list('Year_of_Release').order_by('Year_of_Release').distinct()
        for i in selectYear:
            # i[0].isdigit 
            print('iii[0].isdigit',i[0])
            if i[0] == '0' or i[0] == '1':
                pass
            else:
                yearArr.append(i[0])

        for year in allgenre:
            # print('Count',year[0], year[1])
            genre = year[0]
            if Selectyear:
                genre1 = models.ForecastModel.objects.filter(Year_of_Release=Selectyear, Genre=genre).count() 
            else:
                genre1 = models.ForecastModel.objects.filter(Genre=genre).count() 
            # print('Genre',genre)
            # print('Genre1',genre1)
            arr.append({'genre':genre,'count':genre1})
            # arr.append({"year":Totalyear,'genre':genre,"count":count, 'genre1':genre1})   
        arr.append({'selectYear':yearArr})
        # for year in allyear:
        #     # print('Count',year[0], year[1])
        #     Totalyear = year[0]
        #     genre = year[1]
        #     count = models.ForecastModel.objects.filter(Year_of_Release=Totalyear).values('Global_Sale','Year_of_Release', 'Genre').distinct().aggregate(Sum('Global_Sale'))
        #     genre1 = models.ForecastModel.objects.filter(Year_of_Release=Totalyear).values('Genre') 
        #     # print('genre',genre1)
        #     arr.append({"year":Totalyear,'genre':genre,"count":count, 'genre1':genre1})
        return render(request,'graphGenre.html',{
        'labels': count,
        'FinalSelectYear': Selectyear,
        'data': arr,})


class GraphPredict(views.APIView):
    # template_name = 'graphGenre.html'

    def get(self,request,Selectyear=None):
        data = pd.read_csv("university_records.csv",encoding='latin-1')
        df2 = pd.get_dummies(data)

        df2.head #Check to verify that dummies are ok

        y = df2[['count']]
        x = df2[['year']]

        from sklearn.model_selection import train_test_split
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=0)

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(xtrain, ytrain)
        Yeardata = pd.DataFrame({'year' :[2020,2021,2022,2023,2024,2025]})

        predictions = model.predict(Yeardata)
        newarr = []
                
        gicliniclist = models.ForecastModel.objects.filter()[0]
        count= 0
        Save_arr = []
        arr = []
        allyear = models.ForecastModel.objects.values_list('Year_of_Release', flat=True).order_by('Year_of_Release').distinct()
        for year in allyear:
            count = models.ForecastModel.objects.filter(Year_of_Release=year).values('Global_Sale','Year_of_Release').distinct().aggregate(Sum('Global_Sale'))
            # skip 2 year 
            if year == '2020' or year == '2021' or year == '2022' or year == '2023' or year == '2024' or year == '2025':
                pass
            else:
                arr.append({"year":year,"count":count['Global_Sale__sum']})
            # arr.append({"year":year,"count":count})
            Save_arr.append({"year":year,"count":count['Global_Sale__sum']})

        arr1 = []
        counts = 0
        
        for i in predictions:
            arr.append({'count':i[0], 'year':Yeardata['year'][counts]})
            counts += 1
        
        return render(request,'graphPredict.html',{
        'labels': count,
        'data': arr,})


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        current_datetime = str(datetime.now())
        user = None
        current_datetime=current_datetime.split(" ")
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,'response': recaptcha_response}
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
        	user = authenticate(username=username, password=password)
        else:
                return render(request,'index.html')  
        f=open("./test.log",'a')
        testfile=File(f)
        if user is None:
        	testfile.write("date="+str(current_datetime[0])+" time="+str(current_datetime[1][:-7])+" user=\""+username+"\" Status=failed"+" \n")
        else:
        	testfile.write("date="+str(current_datetime[0])+" time="+str(current_datetime[1][:-7])+" user=\""+username+"\" Status=Pass"+" \n")
        f.close()

        if user is not None:
            login(request,user)
            return redirect('/upload/')
        else:
            return redirect('/')
    return render(request, 'index.html')
def register(request):
	return render(request,'register.html')
def forgetp(request):
	return render(request,'forgetpassword.html')
def signup(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	password1 = request.POST.get('password1')
	current_datetime = datetime.now()  
	if password!=password1:
		return render(request,'register.html')
	else:
		#exist = User.objects.get(username)
		exist="1"
		print(str(exist[0]))
		if str(exist[0]) == str(username):
			print("pass")
			return render(request,'register1.html')
		else:
			print("making")
			user = User.objects.create_user(username,"k",password)
			user.save()
			return render(request,'index.html')

def passwordr(request):
	username1 = request.POST.get('username')
	password1 = request.POST.get('password')
	user=User.objects.get(username=username1)
	user.set_password(password1)
	user.save()
	return render(request,'index.html')			

# Create your views here.
# one parameter named request
# def test(request):
    # return render(request, 'test.html')

class BookListView(generic.ListView):
    model = ForecastModel
    context_object_name = 'my_book_list'   # your own name for the list as a template variable
    queryset = ForecastModel.objects.all()[:5000] # Get 5 books containing the title war
    template_name = 'pagination.html'  # Specify your own template name/location

from django.views.generic import RedirectView

class LogOutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)    


def csv_upload(request):
    # declaring template
    user_list = models.ForecastModel.objects.all()
    template = "csvUpload.html"
    template1 = "pagination.html"
    page = request.GET.get('page', 1)
    print('prrrrrrrrrrrrrrint',page)
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    data = User.objects.all()
    print('daaaaaaaaata',data)
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be Name, platform, Year_of_Release, Genre, Publisher, Global_Sales, Critic_Score, User_Score',
        'profiles': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        page = request.GET.get('page')
        print('page,,',page)
        if page:
            return render(request, template1, { 'users': users })
        else:
            return render(request, template, prompt)
    csv_file = request.FILES['fileInput']
    print('csvvvvvvvvvvvvv',csv_file)
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
        return render(request, template)   
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    productsArr = []

    # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    for column in csv.reader(io_string, delimiter=','):
        if column[2].isdigit() is False:              
            print('column[2].isdigit()',column[2].isdigit(), column[0], column[1],column[2],column[3])
            messages.error(request, 'THIS CSV FILE DOES NOT IN PROPER FORMAT')
            return render(request, template)
        else:
            product = ForecastModel(
                Name=column[0],Platform=column[1],
                Year_of_Release=column[2],Genre=column[3],
                Publisher=column[4],Global_Sale=column[5],
                Critic_Score=column[6],User_Score=column[7]
            )
            productsArr.append(product)  # products are defined before for loop

    if len(productsArr) > 1:
        Total = ForecastModel.objects.bulk_create(productsArr)
        productsArr = []  # clean the list;

    print('Total',Total)
    # articles = ForecastModel.objects.all()
    
    # articles_list = list(articles)[:7000]
    # articles_list1 = list(articles)[7000:10000]
    # articles_list2 = list(articles)[2000:4000]
    # articles_list3 = list(articles)[4000:6000]
    # articles_list4 = list(articles)[6000:8000]
    # articles_list5 = list(articles)[8000:100000]
    # articles_list6 = list(articles)[10000:12000]
    paginator = Paginator(Total, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {

    # 'tables':articles_list,
    'users' : users,
    # 'users' : Total,
    # 'tables1':articles_list1,
    # 'tables2':articles_list2,
    # 'tables3':articles_list3,
    # 'tables4':articles_list4,
    # 'tables5':articles_list5,
    # 'tables6':articles_list6,
    # 'tables': ForecastModel.objects.all()[:16000]
    # 'tables': ForecastModel.objects.values_list('Name','Platform','Year_of_Release','Genre','Publisher','Global_Sale','Critic_Score','User_Score')
    }

        # models.ForecastModel.objects.get_or_create(Name=column[0],Platform=column[1],Year_of_Release=column[2],Genre=column[3],Publisher=column[4],Global_Sale=column[5],Critic_Score=column[6],User_Score=column[7])
    
    # context = {}
    print('runnnnnnnnnn')

    return render(request, template1, context)
 

class GraphPublish(views.APIView):
    template_name = 'graphPublish.html'
    def get(self,request,SelectPublisher=None):
	    gicliniclist = models.ForecastModel.objects.filter()[0]
	    count= 0
	    arr = []
	    yearPub = []
	    allname = models.ForecastModel.objects.values_list('Name','Publisher').order_by('Name').distinct()
	    allpublisher = models.ForecastModel.objects.values_list('Publisher').distinct()
	    selectPublisher = models.ForecastModel.objects.values_list('Publisher').order_by('Publisher').distinct()
	    allgames = models.ForecastModel.objects.values_list('Publisher','Year_of_Release','Name','Global_Sale').order_by('Publisher').distinct()
	    for i in selectPublisher: 
	    	yearPub.append(i[0])
	    for pub2 in allpublisher:
		    publisher = pub2[0]
		    if SelectPublisher:
		    	publish1 = models.ForecastModel.objects.filter(Publisher=SelectPublisher).order_by('Name').distinct()
		    	gs = models.ForecastModel.objects.filter(Publisher=SelectPublisher,Name=publish1).order_by('Global_Sale').distinct()
		    	arr.append({'gs':gs,'Name':publish1})
		    elif SelectPublisher==None:
		        publish1 = models.ForecastModel.objects.filter(Publisher=publisher).count()
		        arr.append({'publisher':publisher,'count':publish1}) 
		    else:
		    	continue
	    arr.append({'SelectPublisher':yearPub})
	    return render(request,'graphPublish.html',{'labels': count,'FinalPublisher': SelectPublisher,'data': arr,})
class GraphPublish1(views.APIView):
    template_name = 'graphPublish1.html'
    def get(self,request,SelectPublisher=None):
	    gicliniclist = models.ForecastModel.objects.filter()[0]
	    count= 0
	    arr = []
	    yearPub = []
	    allg=[]
	    allname = models.ForecastModel.objects.values_list('Name','Publisher').order_by('Name').distinct()
	    allpublisher = models.ForecastModel.objects.values_list('Publisher').distinct()
	    selectPublisher = models.ForecastModel.objects.values_list('Publisher').order_by('Publisher').distinct()
	    allgames = models.ForecastModel.objects.values_list('Publisher','Name','Global_Sale').order_by('Publisher')
	    for i in selectPublisher: 
	    	yearPub.append(i[0])
	    if SelectPublisher:
		    	i=0	
		    	publish1 = models.ForecastModel.objects.filter(Publisher=SelectPublisher).order_by('Name')
		    	allgames1 = models.ForecastModel.objects.filter(Publisher=SelectPublisher).values_list('Publisher','Name','Global_Sale')
		    	c = len(allgames1)
		    	while i < c:
		    		print("pass "+str(i))
		    		gs=allgames1[i][2]
		    		name=allgames1[i][1]
		    		print(allgames1[i])
		    		if name in allg:
			    		i=i+1
			    	else:
				    	print(gs)
				    	print(name)
				    	arr.append({'publisher':name,'count':gs})
				    	allg.append(name)
				    	i=i+1
	    arr.append({'SelectPublisher':yearPub})
	    return render(request,'graphPublish.html',{'labels': count,'FinalPublisher': SelectPublisher,'data': arr,})

############################## future forecast ###############################
