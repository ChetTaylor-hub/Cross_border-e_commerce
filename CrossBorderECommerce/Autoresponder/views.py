import json
import asyncio
from django.shortcuts import render

# Create your views here.

# views.py
from django.core.cache import cache

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from Autoresponder.ozonapi.control import Control

control = Control()
start_flag = False


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to user dashboard
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check active devices
            active_devices = cache.get(f'active_devices_{user.id}', default=0)
            if active_devices >= 2:
                return render(request, 'registration/login_error.html', {'error_message': 'Device limit exceeded.'})
            # Log the user in
            login(request, user)
            # Update active devices count
            cache.incr(f'active_devices_{user.id}')
            return redirect('dashboard')  # Redirect to user dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# views.py
def settle_payment(request):
    # Logic to calculate and settle payment
    # Set Billing.is_paid to True when payment is settled
    return redirect('dashboard')


def main(request):
    return render(request, 'main.html')

def save_settings(request):
    if request.method == 'POST':
        # 处理保存设置的逻辑
        data = json.loads(request.body.decode('utf-8'))

        # 从原始数据中提取所需的键值对
        goods_delivered_interval = data.get('goods_delivered_interval')
        goods_delivered_message = data.get('goods_delivered_message')
        passport_registration_interval = data.get('passport_registration_interval')
        passport_registration_message = data.get('passport_registration_message')
        Api_Key = data.get('Api_Key')
        Client_Id = data.get('Client_Id')
        if Api_Key == '' and Client_Id == '':
            return JsonResponse({'status': 'Api_Key_and_Client_Id_are_empty'})
        if Api_Key == '':
            return JsonResponse({'status': 'Api_Key_is_empty'})
        if Client_Id == '':
            return JsonResponse({'status': 'Client_Id_is_empty'})
            

        # 在这里调用你的 API，将设置保存到数据库或其他存储介质中
        # 这里只是一个示例，实际上需要根据你的需求调用相应的 API
        # 这里假设有一个名为 'save_auto_reply_settings' 的函数来保存设置
        control.save_auto_reply_settings(Client_Id,
                                         Api_Key,
                                         goods_delivered_interval, 
                                         goods_delivered_message,
                                         passport_registration_interval, 
                                         passport_registration_message)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

async def async_view(request):
    if request.method == 'START':
        async def RegisterPassport_reply_task():
            while True:
                control.ReminderRegisterPassportRun()
                # await asyncio.sleep(60 * control.passport_registration_interval)
        async def Delivered_reply_task():
            while True:
                control.ReminderDelivered()
        # 启动异步任务
        asyncio.ensure_future(RegisterPassport_reply_task())
        asyncio.ensure_future(Delivered_reply_task())

        # 你的视图逻辑
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

async def start_auto_reply(request):

    if request.method == 'PUT':
        control.start_auto_reply()
        # 开启自动回复逻辑
        # 这里假设有一个名为 'start_auto_reply' 的函数来启动自动回复

        return JsonResponse({'status': 'success', 'message': 'Auto reply started'})

def stop_auto_reply(request):
    if request.method == 'DELETE':
        # 停止自动回复逻辑
        # 这里假设有一个名为 'stop_auto_reply' 的函数来停止自动回复
        control.stop_auto_reply()
        return JsonResponse({'status': 'success', 'message': 'Auto reply stopped'})

def get_saved_settings(request):
    # 处理获取设置的逻辑
    # 在这里调用你的 API，获取已保存的设置
    # 这里只是一个示例，实际上需要根据你的需求调用相应的 API
    # 这里假设有一个名为 'get_auto_reply_settings' 的函数来获取设置
    settings = control.get_auto_reply_settings()

    # 返回获取的设置数据，用于前端显示
    return JsonResponse(settings)







