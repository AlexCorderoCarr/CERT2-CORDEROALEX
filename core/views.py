from django.shortcuts import render

# Create your views here.
def home(request):

    data ={
        "nombre" : "valeska",
        "apellido" : "cordero",
    }
    return render(request,'core/base.html', data)