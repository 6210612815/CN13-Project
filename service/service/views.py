from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import status
from student.models import Student, StudentForm
from django.urls import reverse
from equipment.models import Equipment
import requests, json, sys


def index(request):
    return render(request, 'index.html')


def homepage(request):
    equipments = Equipment.objects.all()
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})


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
            item.own = person
            item.available = False
            item.save()
            messages.success(request, 'Item booking success.')
        else:
            messages.success(request, 'Item booking fail.')
        return redirect('detail', pk=item_id)

def return_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        userId = request.POST.get('userId')
        item = Equipment.objects.get(id=item_id)
        if item.available == False:
            item.own = None
            item.available = True
            item.save()
            messages.success(request, 'Item return success.')
        else:
            messages.success(request, 'Item return fail.')
        return redirect('detail', pk=item_id)
    

def mybooking(request):
    return render(request, 'mybooking.html')

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