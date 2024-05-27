from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)
