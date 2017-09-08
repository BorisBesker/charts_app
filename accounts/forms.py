from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError('Invalid credentials')
        elif not user.is_active:
            raise forms.ValidationError('Disabled account')
        return super(UserForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self, *args, **kwargs):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('Passwords must match')
        return super(RegisterForm, self).clean(*args, **kwargs)

    def clean_email(self, *args, **kwargs):
        email_qs = User.objects.filter(email=self.cleaned_data['email'])
        if email_qs.exists():
            raise forms.ValidationError('This email has already been registered')
        return self.cleaned_data['email']

    def clean_username(self, *args, **kwargs):
        user_qs = User.objects.filter(username=self.cleaned_data['username'])
        if user_qs.exists():
            raise forms.ValidationError('This username already exists')
        return self.cleaned_data['username']
