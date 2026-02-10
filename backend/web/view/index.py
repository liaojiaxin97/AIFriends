from djiango.shortcuts import render


#跟templates/index.html对应
def index(request):
    return render(request, 'index.html')
