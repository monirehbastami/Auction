from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Item  

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = ''


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'duration', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Item Name'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Duration (e.g., 2 days)'}),
        }
        help_texts = {
            'duration': "Enter the auction duration in one of the following formats: "
                        "'X days' (or 'Xd'), 'X hours' (or 'Xh'), 'X minutes' (or 'Xm'). "
                        "Examples: '2 days', '1h', '30 min'."
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'name', 'description', 'duration']
        widgets = {
            'image': forms.FileInput(), 
        }
