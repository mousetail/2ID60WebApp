from django import forms

class ProfilePhotoForm(forms.Form):
    ## def __init__(self, *args, **kwargs):
    ##    kwargs["label_suffix"] = ""
    ##    super().__init__(self, *args, **kwargs)
    ##    if len(args)==0:
    ##        assert not self.is_bound, str(kwargs)+", "+str(self.__dict__)

    image = forms.ImageField(label="browse", widget=forms.FileInput(attrs={"accept": "image/*"}))
