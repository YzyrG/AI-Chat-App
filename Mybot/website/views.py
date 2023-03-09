from django.shortcuts import render


def home(request):
    language_list = ['bash', 'c', 'clike', 'cpp', 'csharp', 'css', 'csv', 'django', 'docker', 'git', 'go', 'http', 'java', 'javascript', 'json', 'json5', 'latex', 'markdown', 'markup', 'matlab', 'mongodb', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'sql', 'swift', 'vim']
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']
        return render(request, 'home.html', {'language_list':language_list, 'code': code, 'language': language})

    return render(request, 'home.html', {'language_list':language_list})

