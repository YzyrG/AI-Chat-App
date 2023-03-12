from .models import PreviousChat
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
import requests
import os
import json


def home(request):
    # 处理提交表单后得到的表单数据
    if request.method == "POST":
        question = request.POST['question']
        task = request.POST['task']

        if task == '选择任务和A.I. Bot对话吧！':
            messages.success(request, "你忘记选择任务了！")
            # 仍然要返回question，否则用户之前写的问题没了不太友好
            return render(request, 'home.html', {'question': question})

        # 若用户选择陪我聊天任务并提交, 则调用chatsonic api处理表单数据
        elif task == '陪我聊天':
            try:
                # 开始新的一次聊天时历史数据为空list
                history_data = []
                # 以下参考Writesonic官方文档调用ChatSonic api
                url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium&language=zh"
                key = os.getenv("WRITESONIC_API_KEY")

                payload = {
                    "enable_google_results": "true",
                    "enable_memory": True,
                    "input_text": question,
                    "history_data": history_data
                }

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "X-API-KEY": key
                }

                response = requests.post(url, json=payload, headers=headers)

                # 将chatsonic返回的结果转换为dict类型
                response = eval(response.text)
                # 获取返回的message, 即ChatSonic的回复
                answer = response['message']

                # 当前的问题和回复作为下一次继续聊天时的历史数据
                previous_user_chat = {
                    "is_sent": True,
                    "message": question
                }
                previous_sonic_chat = {
                    "is_sent": False,
                    "message": answer
                }
                # 将本次聊天数据存入历史数据中
                history_data.append(previous_user_chat)
                history_data.append(previous_sonic_chat)

                # 使用json将list转换为json字符串
                history_str = json.dumps(history_data)

                # 保存到数据库
                data = PreviousChat(question=question, answer=answer, history_str=history_str)
                data.save()

                return render(request, 'home.html', {'task': task, 'question': question, 'answer': answer})

            except Exception as e:
                # 出错时给answer传e, 使回复区域显示error
                return render(request, 'home.html', {'question': question, 'answer': e})

        # 若用户选择继续聊天任务并提交, 则调用chatsonic api处理表单数据
        elif task == '继续聊天':
            try:

                # 获取数据库最后一条数据，拿到最新的history_str
                history_str = PreviousChat.objects.last().history_str
                print(type(history_str))
                print(history_str)
                # 使用json将str转换为list
                history_data = json.loads(history_str)
                print(type(history_data))
                print(history_data)

                # 以下参考Writesonic官方文档调用ChatSonic api
                url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium&language=zh"
                key = os.getenv("WRITESONIC_API_KEY")

                payload = {
                    "enable_google_results": "true",
                    "enable_memory": True,
                    "input_text": question,
                    "history_data": history_data
                }

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "X-API-KEY": key
                }

                response = requests.post(url, json=payload, headers=headers)

                # 将chatsonic返回的结果转换为dict类型
                response = eval(response.text)
                # 获取返回的message, 即ChatSonic的回复
                answer = response['message']

                # 当前的问题和回复作为下一次继续聊天时的历史数据
                previous_user_chat = {
                    "is_sent": True,
                    "message": question
                }
                previous_sonic_chat = {
                    "is_sent": False,
                    "message": answer
                }
                # 将本次聊天数据存入历史数据中
                history_data.append(previous_user_chat)
                history_data.append(previous_sonic_chat)

                # 使用json将list转换为json字符串
                history_str = json.dumps(history_data)

                # 保存到数据库
                data = PreviousChat(question=question, answer=answer, history_str=history_str)
                data.save()

                return render(request, 'home.html', {'task': task, 'question': question, 'answer': answer})
            except Exception as e:
                # 出错时给answer传e, 使回复区域显示error
                return render(request, 'home.html', {'question': question, 'answer': e})

        # 若用户选择帮我写作任务并提交, 则调用writesonic api处理表单数据
        elif task == '帮我写作':
            try:
                pass
            except Exception as e:
                # 出错时给answer传e, 使回复区域显示error
                return render(request, 'home.html', {'question': question, 'answer': e})

    return render(request, 'home.html')


def history(request):
    # 获取历史数据
    history_data = PreviousChat.objects.all()

    # 设置页数, 煤每页展示10条历史数据
    p = Paginator(PreviousChat.objects.all(), 10)
    # 拿到所请求的页码
    page = request.GET.get('page')
    # 拿到所请求页码的页面内容，return时返回
    pages = p.get_page(page)

    # 获取页数,有多少页就有多少个字符a，便于在history page遍历
    nums = "a" * pages.paginator.num_pages

    return render(request, 'history.html', {"history_data": history_data, 'pages': pages, 'nums': nums})


def delete_history(request, history_id):
    delete_data = PreviousChat.objects.get(id=history_id)
    delete_data.delete()
    messages.success(request, "删除成功！")
    return redirect('history')


# 以下用户注册登录验证功能参考django官方文档
def login_user(request):
    # 获取表单数据
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 验证用户名及密码
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, " (｡･∀･)ﾉﾞ嗨， 您已成功登录！")
            return redirect('home')
        else:
            messages.success(request, " (っ °Д °;)っ 登录失败！请重新登录。")
            return redirect('home')
    else:
        return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, "您已退出登录，Bye！(●'◡'●)")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "您已注册成功！")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
