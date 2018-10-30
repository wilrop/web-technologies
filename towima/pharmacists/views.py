from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib.auth.models import User

def pharmacists_list(request):
    args = {'pharmacist_list': Profile.objects.filter(user_type='Pharmacist')}
    return render(request, 'pharmacists/list.html', args)

def pharmacists_profile(request, pk):
    pharmacist = User.objects.get(pk=pk)
    args = {'pharmacist': pharmacist}
    return render(request, 'pharmacists/profile.html', args)