from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model



User=get_user_model()
class Userform(UserCreationForm):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'placeholder':'Last-name',
        'class':'form-control'
    }))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class':'form-control'
    }))
    
    first_name=forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder':'First-name',
        'class':'form-control'
    }))
    
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'placeholder':'Last-name',
        'class':'form-control'
    }))

    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'Photo'
        ]
    def __init__(self, *args, **kwargs):
        super(Userform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder']='username'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['first_name'].widget.attrs['class']='form-control'
        self.fields['last_name'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['Photo'].widget.attrs['class']='form-control'
       

