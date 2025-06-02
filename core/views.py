from django.shortcuts import render, redirect
from .models import Material, Solicitud 
from django.db.models import Count  
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SolicitudForm
from django.http import HttpResponseForbidden

# Create your views here.
def metricas(request):
    solicitudes_por_mes = (
        Solicitud.objects
        .extra(select={'mes': "strftime('%%Y-%%m', fecha_creacion)"})
        .values('mes')
        .annotate(total= Count('id'))
        .order_by('mes')
    )

    materiales_mas_solicitados = (
        Solicitud.objects
        .values('material__nombre')
        .annotate(total= Count('material'))
        .order_by('-total')[:5]
    )
    data = {
        'solicitudes_por_mes': solicitudes_por_mes,
        'materiales_mas_solicitados': materiales_mas_solicitados
    }
    return render(request, 'core/metricas.html', data)


def home(request):
    return render(request, 'core/base.html', {
        'mostrar_portal': True
    })


def informacion(request):
    materiales = Material.objects.all()
    data = {
        'materiales': materiales
    }
    return render(request, 'core/informacion.html', data)


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


@login_required
def nueva_solicitud(request):
    # Evitar acceso de operarios
    if request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("Acceso denegado: Solo ciudadanos pueden usar esta función.")

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.ciudadano = request.user
            solicitud.save()
            return redirect('mis_solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'core/nueva_solicitud.html', {'form': form})

@login_required
def mis_solicitudes(request):
    # Evitar acceso de operarios
    if request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("Acceso denegado: Solo ciudadanos pueden usar esta función.")

    solicitudes = Solicitud.objects.filter(ciudadano=request.user).order_by('-fecha_creacion')
    return render(request, 'core/mis_solicitudes.html', {'solicitudes': solicitudes})



