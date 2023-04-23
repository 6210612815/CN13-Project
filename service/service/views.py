from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from student.models import Student, StudentForm
from equipment.models import Equipment
from statistic.models import Statistic
from datetime import datetime, timedelta
from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests, json, sys

def lineapi(request):
    try :
        access_token = request.POST.get('access_token')
        params = {
            'access_token': access_token,
        }
        check_verify_response = requests.get('https://api.line.me/oauth2/v2.1/verify', params=params)

        if check_verify_response.status_code == status.HTTP_200_OK:
            headers = {
                'Authorization':f'Bearer {access_token}',
            }
            response = requests.get('https://api.line.me/v2/profile', headers=headers)
            userId = json.loads(response.text)["userId"]

            data = {
                "in_db": Student.objects.filter(userId=userId).exists()
            }

            return HttpResponse(json.dumps(data), content_type='application/json')  

    except Exception as e:
        print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno,str(e)))
        return HttpResponse(json.dumps({'message': 'Get some errors'},default=str), content_type="application/json")

def index(request):
    return render(request, 'index.html')

def category(request):
    return render(request, 'category.html')

def profile(request):
    return render(request, 'profile.html')

def service(request):
    return render(request, 'service.html')

def homepage(request):
    equipments = Equipment.objects.all()
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})

def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        print('post')
        if form.is_valid():
            print("saved")
            form.save()
            return render(request, 'homepage.html')
    else:
        form = StudentForm()
    return render(request, 'register.html', {'form': form})

def detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'detail.html', {'equipment': equipment})

def booking_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        item = Equipment.objects.get(id=item_id)
        if item.available == True:
            #Changing Equipment Models
            item.own = person
            item.available = False
            item.save()

            #Sent Notification to chat "Booking Success"
            ACCESS_TOKEN = 'nRM+jswJLKE7NKjHM1XQTs9oh2f+5iKLtM77Nzrufy8Dx1D710UWp28D0qbIzC9srHUdLAX4ReEue8UlcR6mdFbQPJF0U8Qp4TGxb76wwNIgVUl0l5vd6sCiDsjY7RRuae6OvwRija5/+DnF972L8AdB04t89/1O/w1cDnyilFU='
            USER_ID = userId
            MESSAGE = {'type': 'text', 'text': 'Your Booking is Success'}
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            }
            data = {
                'to': USER_ID,
                'messages': [MESSAGE]
            }
            requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)

            #Add to Statistic Models
            statistic = Statistic(owner=person, item=item, return_datetime=None)
            statistic.save()
            messages.success(request, 'Item booking success.')
        else:
            messages.success(request, 'Item booking fail.')
        return redirect('detail', pk=item_id)

def mybooking(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        statistic = Statistic.objects.filter(owner=person)
        return render(request, 'mybooking.html', {'statistic': statistic})
        
def history(request):
    return render(request, 'history.html')   

def search(request):
    query = request.GET.get('q')
    equipment = Equipment.objects.filter(name__icontains=query)
    return render(request, 'detail.html', {'equipment': equipment})