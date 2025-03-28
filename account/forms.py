from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms

from .models import Customer, MyClient


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    full_name = forms.CharField(max_length=200, help_text='Required', error_messages={
        'required': 'Sorry, you will need to add your name'})
    country = forms.CharField(max_length=200)
    # email = forms.EmailField(max_length=100, help_text='Required', error_messages={
    #     'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ('email', 'full_name', 'country',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'A user with this email already exist, please try another email')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'name': 'email', 'id': 'id_email'})
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'name': 'name', 'id': 'id_name'})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control mb-3',  'name': 'country', 'id': 'id_country'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3'})


class CustomerChangePasswordForm(PasswordChangeForm):

    # def clean_new_password1(self):
    #     password = self.cleaned_data.get("new_password1")
    #     if len(password) < 12:
    #         raise forms.ValidationError("Password must be at least 12 characters.")
    #     return password
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})


class ClientForm(forms.ModelForm):
    class Meta:
        model = MyClient
        fields = '__all__'
        exclude = ['c_address', 'c_created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})
    
    
