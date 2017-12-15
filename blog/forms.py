from django import forms

class ProfilePhotoForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={"accept":"image/*"}))
