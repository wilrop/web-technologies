from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from accounts.models import Profile

# This class will create a signup form, from an existing template provided by django.
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=12)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length = 50)
    user_types = (('Pharmacist', 'Pharmacist'), ('Customer', 'Customer'))
    user_type = forms.ChoiceField(widget=forms.Select, choices=user_types)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'user_type', 'phone_number', 'email', 'password1', 'password2') # The order of the fields

    # A custom save function, so that the user data, as well as additional profile data is saved in the database.
    def save(self, commit = True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data['phone_number']
        date_of_birth = self.cleaned_data['date_of_birth']
        address = self.cleaned_data['address']
        user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            profile = Profile(user=user, phone_number=phone_number, date_of_birth=date_of_birth, address=address, user_type=user_type) # Create a new profile.            
            profile.save()  
        return user


class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
