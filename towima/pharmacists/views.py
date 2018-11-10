from django.shortcuts import render, redirect
from accounts.models import Profile
from pharmacists.forms import PharmacyForm
from django.contrib.auth.models import User


def pharmacists_list(request):
    args = {'pharmacist_list': Profile.objects.filter(user_type='Pharmacist')}
    return render(request, 'pharmacists/list.html', args)

def pharmacists_profile(request, pk):
    pharmacist = User.objects.get(pk=pk)
    args = {'pharmacist': pharmacist}
    return render(request, 'pharmacists/profile.html', args)

def find_pharma(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    if request.method == 'POST':                # When we POST the form.
        form = PharmacyForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            return redirect ('home') 
    else:                                       
        form = PharmacyForm() 
    return render(request, 'pharmacists/find_pharma.html', {'mapbox_access_token': mapbox_access_token, 'form': form})


    