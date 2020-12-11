from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    property_slug = forms.CharField(initial='class', max_length=100, widget = forms.HiddenInput())

    class Meta:
        model = Message
        labels = {
            "message":"Type your message"
        }
        fields = ["message"]
        widgets = {
          'message': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }


class MessageReplyForm(forms.ModelForm):
    conversation_id = forms.CharField(initial='class', max_length=100, widget = forms.HiddenInput())

    class Meta:
        model = Message
        labels = {
            "message":"Type your message"
        }
        fields = ["message"]
        widgets = {
          'message': forms.Textarea(attrs={'rows':5, 'cols':15}),
        }
