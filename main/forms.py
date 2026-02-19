from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}))
    asunto = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aquí...', 'rows': 5}))