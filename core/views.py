from django.shortcuts import render

# Create your views here.
def home(request):

    data ={
        "nombre" : "valeska",
        "apellido" : "cordero",
    }
    return render(request,'core/base.html', data)


def materiales(request):
    materiales = []
    materiales.append({
        "codigo" : "PAP",
        "nombre" : "Papel y cartón",
        "descripcion" : "Incluye cajas, hojas, periódicos, cuadernos (sin espirales ni plásticos)."
    })
    materiales.append({
        "codigo" : "PLAS",
        "nombre" : "Plásticos reciclables",
        "descripcion" : "Botellas PET, envases de alimentos, tapas plásticas. No se aceptan bolsas ni film."
    })
    data = {
        "materiales" : materiales
    }
    return render(request,'core/materiales.html', data)