
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import StudyModel
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
import pytz
import datetime
import calendar
from .forms import SpendingForm, RivalForm
import io
import matplotlib.pyplot as plt
import numpy as np
# Create your views here.

#matplotlibの日本語文字化けを防ぐ
plt.rcParams["font.family"] = "IPAexGothic"


#サインアップ
def signupfunc(request):
    if request.method == 'POST':
        username_list = request.POST.get('username')
        password_list = request.POST.get('password')
        try:
            User.objects.get(username=username_list)
            return render(request, 'signup.html',{'error':'このユーザーは登録されています。'}) 
        except:
            user = User.objects.create_user(username_list, '', password_list)
            return render(request,'signup.html', {})

    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == 'POST':
        username_list = request.POST.get('username')
        password_list = request.POST.get('password')
        user = authenticate(request, username=username_list, password=password_list)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')

    return render(request, 'login.html')

TODAY = str(timezone.now()).split('-')

@login_required
def listfunc(request, year=TODAY[0], month=TODAY[1]):
    study = StudyModel.objects.all().order_by('date')
    author = request.user.get_username()

    for s in study:
        date = str(s.date).split(' ')[0]
        s.date = '/'.join(date.split('-')[1:3])

    form = SpendingForm()
    context = {'year' : year,
            'month' : month,
            'study' : study,
            'form' : form
            }

    if request.method == 'POST':    # フォームでデータが送られてきたら
        data = request.POST
        date = data.get('date')
        subject = data['subject']
        study_time = data['study_time']
        content = data['content']
        date = timezone.datetime.strptime(date, "%Y/%m/%d")
        
        StudyModel.objects.create( 
                date = date,
                subject = subject,
                study_time = study_time,
                content = content,
                author = author
                )
        return redirect('list') 

    return render(request, 'list.html', context)     

def logoutfunc(request):
    logout(request)
    return redirect('login')


def mypagefunc(request):
    year,month = TODAY[0], TODAY[1]
    #study -> ユーザーごとの今月だけのデータ
    study = StudyModel.objects.filter(author__iexact=request.user.get_username(), date__month=month).order_by('date')
    #study_all -> ユーザーごとの全てのデータ
    study_all = StudyModel.objects.filter(author__iexact=request.user.get_username())

    day = [i for i in range(1, calendar.monthrange(int(year), int(month))[1] + 1)]
    month_time = [0 for i in range(len(day))]
    for s in study:
        month_time[int(str(s.date).split('-')[2][:3])-1] += int(s.study_time)

    plt.figure()
    plt.bar(day, month_time, color='#6a5acd', align='center')
    plt.grid(True)
    plt.xlim([0, 31])
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Study Time', fontsize=16)
    #ローカルに画像を保存
    plt.savefig('D:/Django/study_logger/media/studytime_me.svg',format='svg',transparent=True)

    #ライバルのユーザー名を取得
    rival_name = request.GET.get('rival')
    try:
        rival_data = StudyModel.objects.filter(author__icontains=rival_name,date__month=month).order_by('date')
        print('rival_data',rival_data)
        print('a',rival_data[0].get_subject_display)
    except:
        rival_data = StudyModel.objects.filter(author__icontains=request.user.get_username(),date__month=month).order_by('date')

    context = {'year' : year,
            'month' : month,
            'study' : study,
            'rival' :rival_data
           }

    return render(request, 'mypage.html', context)