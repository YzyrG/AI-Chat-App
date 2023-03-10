from django.shortcuts import render
from django.contrib import messages
import requests
import os


def home(request):
    # 处理提交表单后得到的表单数据
    if request.method == "POST":

        question = request.POST['question']
        task = request.POST['task']

        print(task)

        # 若用户未选择language就提交, 则给出提示
        if task == '选择任务和A.I. Bot对话吧！':
            messages.success(request, "你忘记选择任务了！")
            # 仍然要返回code，否则用户之前写的代码全没了会生气，不太友好
            return render(request, 'home.html', {'question': question})

        # 若用户选择任务并提交, 则调用writesonic api处理已提交的表单数据
        else:
            try:

                # 以下参考Writesonic官方文档调用ChatSonic api
                url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium&language=zh"
                key = os.getenv("WRITESONIC_API_KEY")

                payload = {
                    "enable_google_results": "true",
                    "enable_memory": True,
                    "input_text": question
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
                return render(request, 'home.html', {'task': task,  'question': question, 'answer': answer})
            except Exception as e:
                # 出错时给code传e, 使code区域显示error
                return render(request, 'home.html', {'question': question})
    return render(request, 'home.html')
