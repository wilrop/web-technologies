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
        fields = (              # The order of the fields
            'username', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'user_type', 
            'phone_number', 
            'email', 
            'password1', 
            'password2') 

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


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=12)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length = 50)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = self.instance.profile.phone_number
        self.fields['date_of_birth'].initial = self.instance.profile.date_of_birth
        self.fields['address'].initial = self.instance.profile.address

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'email',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.date_of_birth = self.cleaned_data['date_of_birth']
        user.profile.address = self.cleaned_data['address']

        if commit:
            user.save() 
            user.profile.save()

        return user
