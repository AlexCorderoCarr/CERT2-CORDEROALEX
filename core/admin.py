from django.contrib import admin
from .models import Material, Solicitud

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion')
    search_fields = ('codigo', 'nombre')

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'ciudadano', 'material', 'cantidad', 'fecha_estimada', 'estado', 'operario_asignado')
    list_filter = ('estado', 'material', 'operario_asignado')
    search_fields = ('ciudadano__username', 'material__nombre')
    list_editable = ('estado', 'operario_asignado')
    readonly_fields = ('fecha_creacion',)

