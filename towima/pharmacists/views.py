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
    