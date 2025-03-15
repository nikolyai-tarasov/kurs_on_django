from django import forms

from mailings.models import Recipient, Message, Newsletter


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment', 'avatar', ]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'letter', ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['letter'].widget.attrs.update({'class': 'form-control'})


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['first_shipment', 'last_dispatch', 'status', 'message', 'recipients']

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields['first_shipment'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})
        self.fields['last_dispatch'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-control', 'multiple': 'multiple'})


class NewsletterModeratorForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['status', ]
