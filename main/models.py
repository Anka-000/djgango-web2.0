#from django.db import models

# Create your models here.
#class area(models.Model):
#    area_id = models.AutoField(primary_key=True)
#    area_nombre = models.CharField(max_length=200)
#    area_descripcion = models.TextField()

#    def __str__(self):
#        return self.area_nombre

from django.db import models
import os

class Area(models.Model):
    # Opciones para el selector
    CATEGORIAS = [
        ('transparencia', 'Obligaciones de Transparencia'),
        ('financiera', 'Información Financiera'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre del Área")
    # --- CAMPO NUEVO ---
    categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIAS, 
        default='transparencia', 
        verbose_name="Sección a la que pertenece"
    )
    # -------------------
    descripcion = models.TextField(blank=True, verbose_name="Descripción (Opcional)")
    slug = models.SlugField(unique=True, verbose_name="Identificador URL (automático)")

    class Meta:
        verbose_name = "Área / Departamento"
        verbose_name_plural = "Áreas / Departamentos"
        ordering = ['-nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

class TipoDocumento(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='tipos_documento', verbose_name="Pertenece al Área")
    nombre = models.CharField(max_length=200, verbose_name="Tipo de Documento")
    slug = models.SlugField(verbose_name="Identificador URL")
    class Meta:
        unique_together = ('area', 'slug')
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    

class Documento(models.Model):
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='documentos', verbose_name="Tipo de Documento")
    titulo = models.CharField(max_length=255, verbose_name="Título del Documento")
    fecha_publicacion = models.DateField(verbose_name="Fecha de Publicación")
    archivo_pdf = models.FileField(upload_to='documentos/%Y/%m/', verbose_name="Archivo PDF")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['titulo']
    def __str__(self):
        return self.titulo
    
class DatoPersonal(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Nombre del Documento")
    archivo_pdf = models.FileField(upload_to='datos_personales/', verbose_name="Archivo PDF")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dato Personal (PDF)"
        verbose_name_plural = "Datos Personales"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo
    
class DocumentoDestacado(models.Model):
    OPCIONES = [
        ('organigrama', 'Organigrama'),
        ('tabla_aplicabilidad', 'Tabla de Aplicabilidad'),
    ]
    
    tipo = models.CharField(max_length=30, choices=OPCIONES, unique=True, verbose_name="Tipo de Documento")
    archivo_pdf = models.FileField(upload_to='destacados/', verbose_name="Archivo PDF")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento Destacado"
        verbose_name_plural = "Documentos Destacados (Organigrama/Tabla)"

    def __str__(self):
        return self.get_tipo_display()