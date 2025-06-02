from django.contrib import admin
from .models import Material, Solicitud
from django.contrib.auth.models import User, Group
from django.contrib.admin import SimpleListFilter

class OperarioFilter(SimpleListFilter):
    title = 'Operario asignado'
    parameter_name = 'operario_asignado'

    def lookups(self, request, model_admin):
        try:
            operarios = Group.objects.get(name="Operarios").user_set.all()
            return [(op.id, op.username) for op in operarios]
        except Group.DoesNotExist:
            return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(operario_asignado__id=self.value())
        return queryset
    
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion')
    search_fields = ('codigo', 'nombre')


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'ciudadano', 'material', 'cantidad', 'fecha_estimada', 'estado', 'operario_asignado')
    list_filter = ('estado', 'material', OperarioFilter)
    search_fields = ('ciudadano__username', 'material__nombre')
    list_editable = ('estado', 'operario_asignado')
    readonly_fields = ('fecha_creacion',)
    fields = (
        'ciudadano', 'material', 'cantidad', 'fecha_estimada',
        'estado', 'comentario_operario', 'operario_asignado', 'fecha_creacion'
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "operario_asignado":
            try:
                operarios = Group.objects.get(name="Operarios").user_set.all()
                kwargs["queryset"] = operarios
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_staff:
            return qs.filter(operario_asignado=request.user)
        return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        if request.user.is_staff:
            return self.readonly_fields + (
                'ciudadano',
                'material',
                'cantidad',
                'fecha_estimada',
                'operario_asignado'
            )
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.operario_asignado == request.user:
            return True
        return False
