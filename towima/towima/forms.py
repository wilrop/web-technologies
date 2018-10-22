from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from towima.models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=12)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length = 50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'email', 'password1', 'password2', )

    def save(self, commit = True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data['phone_number']
        date_of_birth = self.cleaned_data['date_of_birth']
        address = self.cleaned_data['address']
        if commit:
            user.save()
            profile = Profile(user=user, phone_number=phone_number, date_of_birth=date_of_birth, address=address)
            profile.save()  
        return user
