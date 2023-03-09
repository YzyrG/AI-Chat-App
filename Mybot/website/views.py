from django.shortcuts import render
from django.contrib import messages


def home(request):

    # 用户可选择的编程语言list
    language_list = ['bash', 'c', 'clike', 'cpp', 'csharp', 'css', 'csv', 'django', 'docker', 'git', 'go', 'http', 'java', 'javascript', 'json', 'json5', 'latex', 'markdown', 'markup', 'matlab', 'mongodb', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'sql', 'swift', 'vim']
    # 处理提交表单后得到的表单数据
    if request.method == "POST":

        code = request.POST['code']
        language = request.POST['language']

        # 若用户未选择language就提交则给出提示
        if language == 'Select Programming Language':
            messages.success(request, "You should choose a programming language...")
            # 仍然要返回code，否则用户之前写的代码全没了会生气，不太友好
            return render(request, 'home.html', {'language_list':language_list, 'code': code, 'language': language})

        return render(request, 'home.html', {'language_list':language_list, 'code': code, 'language': language})

    return render(request, 'home.html', {'language_list':language_list})

