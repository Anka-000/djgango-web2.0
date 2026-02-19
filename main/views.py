#from django.shortcuts import render
#from django.http import HttpResponse
#from .models import area
# Create your views here.
#def homepage(request):
#    return render(request=request,
#                  template_name="main/home.html",
#                  context={"areas": area.objects.all()})


from django.shortcuts import render, get_object_or_404
from .models import Area, TipoDocumento, Documento, DatoPersonal, DocumentoDestacado
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactoForm

# 1. Página de Inicio con formulario de contacto
def inicio(request):
    doc_organigrama = DocumentoDestacado.objects.filter(tipo='organigrama').first()
    doc_tabla = DocumentoDestacado.objects.filter(tipo='tabla_aplicabilidad').first()
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Extraemos los datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            
            # Formateamos cómo se verá el mensaje en la bandeja de entrada
            mensaje_completo = f"Has recibido un nuevo mensaje desde el Portal Municipal.\n\nDe: {nombre} <{correo}>\n\nMensaje:\n{mensaje}"
            
            try:
                # Enviamos el correo
                send_mail(
                    subject=f"Portal Web: {asunto}",
                    message=mensaje_completo,
                    from_email=settings.EMAIL_HOST_USER, # El cartero (configurado en settings)
                    recipient_list=['transparenciastgver@outlook.com'], # Destinatario fijo 
                    fail_silently=False,
                )
                # Mensaje de éxito para el usuario
                messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Nos pondremos en contacto pronto.')
                return redirect('inicio') # Recarga la página limpia
            except Exception as e:
                # Mensaje de error si falla el envío
                messages.error(request, 'Hubo un error al enviar tu mensaje. Intenta de nuevo más tarde.')
    else:
        # Si entra por primera vez a la página, mostramos el formulario vacío
        form = ContactoForm()

    return render(request, 'main/inicio.html', {
        'form': form, # El de tu contacto
        'doc_organigrama': doc_organigrama,
        'doc_tabla': doc_tabla
    })



# 2. Obligaciones de Transparencia (Solo muestra Áreas de categoría 'transparencia')
def lista_transparencia(request):
    areas = Area.objects.filter(categoria='transparencia')
    # Cambiamos 'lista_areas.html' por 'transparencia.html'
    return render(request, 'main/transparencia.html', {'areas': areas})

# 3. Información Financiera (Solo muestra Áreas de categoría 'financiera')
def lista_financiera(request):
    areas = Area.objects.filter(categoria='financiera')
    # Cambiamos 'lista_areas.html' por 'financiera.html'
    return render(request, 'main/financiera.html', {'areas': areas})

# 4. Datos Personales (Lista simple de PDFs)
def lista_datos_personales(request):
    documentos = DatoPersonal.objects.all()
    return render(request, 'main/datos_personales.html', {'documentos': documentos})

# 6. Lista de todas las áreas 
def lista_areas(request):
    areas = Area.objects.all()
    return render(request, 'main/lista_areas.html', {'areas': areas})

# 7. Dentro de un área, mostrar los tipos de documentos
def detalle_area(request, area_slug):
    area = get_object_or_404(Area, slug=area_slug)
    # Obtenemos los tipos de documento asociados a esta área
    tipos = area.tipos_documento.all() 
    return render(request, 'main/detalle_area.html', {'area': area, 'tipos': tipos})

# 8. Lista de PDFs dentro de un tipo específico
def lista_documentos(request, area_slug, tipo_slug):
    area = get_object_or_404(Area, slug=area_slug)
    tipo = get_object_or_404(TipoDocumento, slug=tipo_slug, area=area)
    # Gracias al 'ordering' en el modelo, ya vienen ordenados por fecha descendente
    documentos = tipo.documentos.all()
    
    return render(request, 'main/lista_documentos.html', {
        'area': area,
        'tipo': tipo,
        'documentos': documentos
    })

def consulta_obras(request):
    return render(request, 'main/consulta_obras.html')

def comite_transparencia(request):
    return render(request, 'main/comite_transparencia.html')