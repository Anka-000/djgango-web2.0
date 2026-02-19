"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#from django.urls import path
#from . import views

#app_name = 'main'

#urlpatterns = [
#    path('', views.homepage, name='homepage'),
#]



from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'), # Home
    path('transparencia/', views.lista_transparencia, name='lista_transparencia'),
    path('financiera/', views.lista_financiera, name='lista_financiera'),
    path('datos-personales/', views.lista_datos_personales, name='lista_datos_personales'),
    path('area/<slug:area_slug>/', views.detalle_area, name='detalle_area'),
    path('area/<slug:area_slug>/<slug:tipo_slug>/', views.lista_documentos, name='lista_documentos'),
    path('consulta-obras/', views.consulta_obras, name='consulta_obras'),
    path('comite-transparencia/', views.comite_transparencia, name='comite_transparencia'),
]