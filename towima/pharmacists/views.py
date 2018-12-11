from django.shortcuts import render, redirect
from accounts.models import Profile
from pharmacists.models import Rating
from django.contrib.auth.models import User
from pharmacists.forms import CommentForm

def pharmacists_list(request):
    args = {'pharmacist_list': Profile.objects.filter(user_type='Pharmacist')}
    return render(request, 'pharmacists/list.html', args)

def pharmacists_profile(request, pk):
    pharmacist = User.objects.get(pk=pk)
    rated_list = Rating.objects.filter(pharmacist = pharmacist.profile)

    if rated_list:
        acc_rating = 0
        for rating in rated_list:
            acc_rating += rating.rating 
        rating = int(round(acc_rating / len(rated_list)))
    else:
        rating = None
    args = {'pharmacist': pharmacist, 'rating': rating}
    return render(request, 'pharmacists/profile.html', args)

def find_pharma(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    service = Directions()
    origin = {
        'type': 'Feature',
        'properties': {'name': 'Portland, OR'},
        'geometry': {
            'type': 'Point',
            'coordinates': [-122.7282, 45.5801]}}
    destination = {
        'type': 'Feature',
        'properties': {'name': 'Bend, OR'},
        'geometry': {
            'type': 'Point',
            'coordinates': [-121.3153, 44.0582]}}
    if request.method == 'GET': 
        response = service.directions([origin, destination], 'mapbox/driving')
        
    return render(request, 'pharmacists/find_pharma.html', {'mapbox_access_token': mapbox_access_token})

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

def add_rating_to_profile(request, pk, new_rating):
    user = request.user
    pharmacist = User.objects.get(pk=pk) 
    try:
        rating = Rating.objects.get(pharmacist = pharmacist.profile, user=user)
        rating.rating = new_rating
    except Rating.DoesNotExist:
        rating = Rating(user=user, pharmacist=pharmacist.profile, rating=new_rating)
    rating.save()

    return redirect('profile', pk=pk)
    