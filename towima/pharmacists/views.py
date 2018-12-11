from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib.auth.models import User
from pharmacists.forms import CommentForm

def pharmacists_list(request):
    args = {'pharmacist_list': Profile.objects.filter(user_type='Pharmacist')}
    return render(request, 'pharmacists/list.html', args)

def pharmacists_profile(request, pk):
    pharmacist = User.objects.get(pk=pk)
    args = {'pharmacist': pharmacist}
    return render(request, 'pharmacists/profile.html', args)

def add_comment_to_profile(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            form.save(pk, user)
            return redirect('profile', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'pharmacists/add_comment_to_profile.html', {'form': form})


    