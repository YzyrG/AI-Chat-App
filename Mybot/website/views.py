from django.shortcuts import render
from django.contrib import messages
import requests
from .models import PreviousChat
import os


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

                # 以下参考Writesonic官方文档调用ChatSonic api
                url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium&language=zh"
                key = os.getenv("WRITESONIC_API_KEY")

                payload = {
                    "enable_google_results": "true",
                    "enable_memory": True,
                    "input_text": question,
                    "history_data": []
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

                # 保存到数据库
                data = PreviousChat(question=question, answer=answer)
                data.save()

                return render(request, 'home.html', {
                    'task': task,
                    'question': question,
                    'answer': answer,
                })

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
    history_data = PreviousChat.objects.all()

    return render(request, 'history.html', {"history_data": history_data})
