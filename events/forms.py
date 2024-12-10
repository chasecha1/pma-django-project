from django import forms
from .models import File  # Import the File model
from .models import Message

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'title', 'description', 'keywords']

    keywords = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter keywords separated by commas',
            'rows': 1,
            'style': 'width: 100%; resize: none;'
        }),
        required=False
    )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message here...'
            }),
        }