#from django.contrib import admin
#from .models import area
#from tinymce.widgets import TinyMCE
#from django.db import models
# Register your models here.
#class areaAdmin(admin.ModelAdmin):
#    formfield_overrides = {
#        models.TextField: {'widget': TinyMCE()}
#    }

#admin.site.register(area, areaAdmin)

from django.contrib import admin
from .models import Area, TipoDocumento, Documento, DatoPersonal, DocumentoDestacado

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'categoria') 
    list_filter = ('categoria',) 

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'area')
    list_filter = ('area',) # Filtro lateral por área

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_publicacion', 'ver_archivo')
    list_filter = ('tipo__area', 'tipo', 'fecha_publicacion') # Filtros potentes
    search_fields = ('titulo', 'tipo__nombre') # Barra de búsqueda
    date_hierarchy = 'fecha_publicacion' # Navegación por fechas arriba

    def ver_archivo(self, obj):
        from django.utils.html import format_html
        if obj.archivo_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', obj.archivo_pdf.url)
        return "No archivo"
    
@admin.register(DatoPersonal)
class DatoPersonalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_subida')

@admin.register(DocumentoDestacado)
class DocumentoDestacadoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha_actualizacion')