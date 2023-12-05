from django.shortcuts import render

# Create your views here.

# views.py
from django.core.cache import cache

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from Autoresponder.ozonapi.control import Control

control = Control()

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


def index(request):
    '''
    定义一个主页的方法，参数为请求对象
    函数返回经过render渲染的页面index.html
    index.html在blogapp下新建的templates目录中创建
    '''
    return render(request, 'index.html')

def base(request):
    '''
    定义一个主页的方法，参数为请求对象
    函数返回经过render渲染的页面index.html
    index.html在blogapp下新建的templates目录中创建
    '''
    return render(request, 'base/base.html')

from django.http import JsonResponse



def main_1(request):
    # 这里可以编写处理自动回复设置的逻辑，包括保存设置、启动和停止自动回复等操作
    if request.method == 'POST':
        # 处理保存设置的逻辑
        # 获取 POST 请求中的数据
        goods_delivered_interval = request.POST.get('goods_delivered_interval')
        goods_delivered_message = request.POST.get('goods_delivered_message')
        passport_registration_interval = request.POST.get('passport_registration_interval')
        passport_registration_message = request.POST.get('passport_registration_message')

        # 在这里调用你的 API，将设置保存到数据库或其他存储介质中
        # 这里只是一个示例，实际上需要根据你的需求调用相应的 API
        # 这里假设有一个名为 'save_auto_reply_settings' 的函数来保存设置
        control.save_auto_reply_settings(goods_delivered_interval, goods_delivered_message,
                                         passport_registration_interval, passport_registration_message)

        return JsonResponse({'status': 'success'})

    elif request.method == 'GET':
        # 处理获取设置的逻辑
        # 在这里调用你的 API，获取已保存的设置
        # 这里只是一个示例，实际上需要根据你的需求调用相应的 API
        # 这里假设有一个名为 'get_auto_reply_settings' 的函数来获取设置
        settings = control.get_auto_reply_settings()

        # 返回获取的设置数据，用于前端显示
        return JsonResponse(settings)
    
    elif request.method == 'PUT':
        # 开启自动回复逻辑
        # 这里假设有一个名为 'start_auto_reply' 的函数来启动自动回复
        control.start_auto_reply()
        return JsonResponse({'status': 'success', 'message': 'Auto reply started'})

    elif request.method == 'DELETE':
        # 停止自动回复逻辑
        # 这里假设有一个名为 'stop_auto_reply' 的函数来停止自动回复
        control.stop_auto_reply()
        return JsonResponse({'status': 'success', 'message': 'Auto reply stopped'})

    else:
        # 处理其他请求，例如未知的请求类型
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def main(request):
    return render(request, 'main.html')

def save_settings(request):
    if request.method == 'POST':
        # 处理保存设置的逻辑
        # 获取 POST 请求中的数据
        goods_delivered_interval = request.POST.get('goods_delivered_interval')
        goods_delivered_message = request.POST.get('goods_delivered_message')
        passport_registration_interval = request.POST.get('passport_registration_interval')
        passport_registration_message = request.POST.get('passport_registration_message')

        # 在这里调用你的 API，将设置保存到数据库或其他存储介质中
        # 这里只是一个示例，实际上需要根据你的需求调用相应的 API
        # 这里假设有一个名为 'save_auto_reply_settings' 的函数来保存设置
        control.save_auto_reply_settings(goods_delivered_interval, goods_delivered_message,
                                         passport_registration_interval, passport_registration_message)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def start_auto_reply(request):
    if request.method == 'PUT':
        # 开启自动回复逻辑
        # 这里假设有一个名为 'start_auto_reply' 的函数来启动自动回复
        control.start_auto_reply()
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







