from django import forms
from django.db.models import Q
from monkey_hd.models import *


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'description')


class TicketFormClient(forms.ModelForm):
    name = forms.CharField(max_length=120, disabled=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea, disabled=True)

    class Meta:
        model = Ticket
        fields = ('name', 'description')


class TicketFormDeveloper(forms.ModelForm):
    name = forms.CharField(max_length=120, disabled=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea, disabled=True)
    status = forms.ModelChoiceField(Status.objects.all())

    class Meta:
        model = Ticket
        fields = ('name', 'description', 'status')


class TicketFormAdminNew(forms.ModelForm):
    name = forms.CharField(max_length=120)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    priority = forms.ModelChoiceField(Priority.objects.all())
    permission = Permission.objects.get(name='client')
    owner = forms.ModelChoiceField(UserProfile.objects.filter(~Q(permission=permission)))
    status = forms.ModelChoiceField(Status.objects.all())
    scalability = forms.ModelChoiceField(Scalability.objects.all())

    class Meta:
        model = Ticket
        fields = ('name', 'description', 'priority', 'owner', 'status', 'scalability')


class TicketFormAdminEdit(forms.ModelForm):
    name = forms.CharField(max_length=120)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    priority = forms.ModelChoiceField(Priority.objects.all())
    permission = Permission.objects.get(name='client')
    owner = forms.ModelChoiceField(UserProfile.objects.filter(~Q(permission=permission)))
    status = forms.ModelChoiceField(Status.objects.all())
    scalability = forms.ModelChoiceField(Scalability.objects.all())

    class Meta:
        model = Ticket
        fields = ('name', 'description', 'priority', 'creator', 'owner', 'status', 'scalability')


class TicketFormView(forms.ModelForm):
    name = forms.CharField(max_length=120, disabled=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea, disabled=True)
    priority = forms.ModelChoiceField(Priority.objects.all(), disabled=True)
    creator = forms.ModelChoiceField(UserProfile.objects.all(), disabled=True)
    permission = Permission.objects.get(name='client')
    owner = forms.ModelChoiceField(UserProfile.objects.filter(~Q(permission=permission)), disabled=True)
    status = forms.ModelChoiceField(Status.objects.all(), disabled=True)
    scalability = forms.ModelChoiceField(Scalability.objects.all(), disabled=True)

    class Meta:
        model = Ticket
        fields = ('name', 'description', 'priority', 'creator', 'owner', 'status', 'scalability')
