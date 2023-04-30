from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from student.models import Student, StudentForm
from equipment.models import Equipment
from statistic.models import Statistic
from favorites.models import Favorite
from datetime import timedelta
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

def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request, 'about.html')

def sent_list(request):
    return render(request, 'sent_list.html')

def homepage(request):
    equipments = Equipment.objects.all()
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})
    
def homepage_choice(request, choice):
    if request.method == 'GET':
        equipments = Equipment.objects.filter(category=choice)
        return render(request, 'homepage.html', {'equipments': equipments})

def homepage_sort_datetime(request):
    equipments = Equipment.objects.all().order_by('-create_datetime')
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})

def homepage_sort_picked(request):
    equipments = Equipment.objects.all().order_by('-picked')
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})

def homepage_sort_name(request):
    equipments = Equipment.objects.all().order_by('name')
    for item in equipments:
        item.url = reverse('detail', args=[item.pk])
    return render(request, 'homepage.html', {'equipments': equipments})

def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'homepage.html')
    else:
        form = StudentForm()
    return render(request, 'register.html', {'form': form})

def detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if equipment.available == True:
        return render(request, 'detail.html', {'equipment': equipment})
    else:
        statistic = Statistic.objects.get(item=equipment, return_datetime=None)
        return render(request, 'detail.html', {'equipment': equipment,
                                               'statistic': statistic})

def booking_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        userId = request.POST.get('userId')
        d = request.POST.get('date')
        date = int(d)
        person = Student.objects.get(userId=userId)
        item = Equipment.objects.get(id=item_id)
        if item.available == True:
            item.own = person
            item.available = False
            item.picked += 1
            item.save()

            statistic = Statistic(owner=person, item=item, due_datetime=timezone.now()+timedelta(days=date), return_datetime=None)
            statistic.save()

            ACCESS_TOKEN = 'c2Z0ZgjoiytkNVDXPMoS0ze/GPHKNssrdcfTSPIScSpKWETaBewBx925iNoD6LM9LmvvATqYrzmtkPPgECtofhUK0yYaAVKQDDRFsgxlnKf7tyCv9My60BlMahC8lLzDNgEPRJKv1x7d8mfB04zKaAdB04t89/1O/w1cDnyilFU='
            USER_ID = userId
            date_time = statistic.due_datetime
            formatted_date_time = date_time.strftime("%d/%m/%Y")
            MESSAGE = {'type': 'text', 'text': f'Your Booking is Success.\n You booked a {item.name}.\n Due Date : {formatted_date_time}'}
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            }
            data = {
                'to': USER_ID,
                'messages': [MESSAGE]
            }
            requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
            messages.success(request, 'Item booking success.')
        else:
            messages.success(request, 'Item booking fail.')
        return redirect('detail', pk=item_id)

def myfavorite(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        student = Student.objects.get(userId=userId)
        
        try:
            favorite = Favorite.objects.filter(user=student)
            return render(request, 'myfavorite.html', {'favorite': favorite})
        except ValueError as e:
            return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
    return render(request, 'homepage.html')

def mybooking(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        try:
            statistic = Statistic.objects.filter(owner=person)
            return render(request, 'mybooking.html', {'statistic': statistic,
                                                      'now': timezone.now()})
        except ValueError as e:
            return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
    return render(request, 'homepage.html')

def my_booking_not_return(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        try:
            statistic = Statistic.objects.filter(owner=person).filter(return_datetime__isnull=True).filter(due_datetime__gt=timezone.now())
            return render(request, 'mybooking.html', {'statistic': statistic,
                                                      'now': timezone.now()})
        except ValueError as e:
            return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
    return render(request, 'homepage.html')
    
def my_booking_return(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        try:
            statistic = Statistic.objects.filter(owner=person).filter(return_datetime__isnull=False)
            return render(request, 'mybooking.html', {'statistic': statistic,
                                                      'now': timezone.now()})
        except ValueError as e:
            return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
    return render(request, 'homepage.html')

def my_booking_overdue(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        person = Student.objects.get(userId=userId)
        try:
            statistic = Statistic.objects.filter(owner=person).filter(return_datetime__isnull=True).filter(due_datetime__lt=timezone.now())
            return render(request, 'mybooking.html', {'statistic': statistic,
                                                      'now': timezone.now()})
        except ValueError as e:
            return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
    return render(request, 'homepage.html')
    
def search(request):
    query = request.GET.get('q')
    if query:
        item = Equipment.objects.filter(Q(name__icontains=query) | Q(category__icontains=query))
    else:
        item = []
    return render(request, 'homepage.html', {'equipments': item })

def sent_list_to_chat(request):
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
            person = Student.objects.get(userId=userId)

            try:
                statistic = Statistic.objects.filter(owner=person).filter(return_datetime__isnull=True)
                print(statistic)
                if not statistic.exists():
                    ACCESS_TOKEN = 'c2Z0ZgjoiytkNVDXPMoS0ze/GPHKNssrdcfTSPIScSpKWETaBewBx925iNoD6LM9LmvvATqYrzmtkPPgECtofhUK0yYaAVKQDDRFsgxlnKf7tyCv9My60BlMahC8lLzDNgEPRJKv1x7d8mfB04zKaAdB04t89/1O/w1cDnyilFU='
                    USER_ID = userId
                    MESSAGE = {'type': 'text', 'text': f'Your Booking List is Empty.'}
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {ACCESS_TOKEN}'
                    }
                    data = {
                        'to': USER_ID,
                        'messages': [MESSAGE]
                    }
                    requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
                else:
                
                    ACCESS_TOKEN = 'c2Z0ZgjoiytkNVDXPMoS0ze/GPHKNssrdcfTSPIScSpKWETaBewBx925iNoD6LM9LmvvATqYrzmtkPPgECtofhUK0yYaAVKQDDRFsgxlnKf7tyCv9My60BlMahC8lLzDNgEPRJKv1x7d8mfB04zKaAdB04t89/1O/w1cDnyilFU='
                    USER_ID = userId
                    MESSAGE = {'type': 'text', 'text': f'This is Your Booking List.'}
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {ACCESS_TOKEN}'
                    }
                    data = {
                        'to': USER_ID,
                        'messages': [MESSAGE]
                    }
                    requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)

                    for stat in statistic:
                        
                        ACCESS_TOKEN = 'c2Z0ZgjoiytkNVDXPMoS0ze/GPHKNssrdcfTSPIScSpKWETaBewBx925iNoD6LM9LmvvATqYrzmtkPPgECtofhUK0yYaAVKQDDRFsgxlnKf7tyCv9My60BlMahC8lLzDNgEPRJKv1x7d8mfB04zKaAdB04t89/1O/w1cDnyilFU='
                        USER_ID = userId
                        date_time = stat.due_datetime
                        formatted_date_time = date_time.strftime("%d/%m/%Y")
                        MESSAGE = {'type': 'text', 'text': f'Name: {stat.item.name}.\n Due Date: {formatted_date_time}'}
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {ACCESS_TOKEN}'
                        }
                        data = {
                            'to': USER_ID,
                            'messages': [MESSAGE]
                        }
                        requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
                    
                    return HttpResponse(json.dumps({'message': 'Success'}), content_type='application/json') 
            
            except ValueError as e:
                return HttpResponse('Error: Invalid value. Please enter an integer.', status=400)
            
    except Exception as e:
        print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno,str(e)))
        return HttpResponse(json.dumps({'message': 'Get some errors'},default=str), content_type="application/json")

def profile(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        student = Student.objects.get(userId=userId)
        return render(request, 'profile.html', {'student': student})

def edit_profile(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        student.fname = request.POST['fname']
        student.lname = request.POST['lname']
        student.email = request.POST['email']
        student.sid = request.POST['sid']
        student.tel = request.POST['tel']
        student.save()
        return redirect('edit_profile', id=student.id)
    else:
        return render(request, 'profile.html', {'student': student})

def favorite(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        item = request.POST.get('item_id')
        student = Student.objects.get(userId=userId)
        equipment = Equipment.objects.get(id=item)
        try:
            favorite = Favorite.objects.get(user=student, item=equipment)
            favorite.delete()
            message = 'removed'
        except Favorite.DoesNotExist:
            favorite = Favorite.objects.create(user=student,  item=equipment)
            message = 'added'
        return render(request, 'detail.html', {'equipment': equipment,
                                               'favorite': favorite})
    
