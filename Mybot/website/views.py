from django.shortcuts import render


def home(request):
    language_list = [' python', 'c', 'cpp', 'css', 'django', 'git', 'go', 'java', 'javascript', 'markup', 'mongodb', 'powershell', 'r', 'regex', 'ruby', 'rust', 'sql', 'swift']

    return render(request, 'home.html', {'language_list':language_list})

