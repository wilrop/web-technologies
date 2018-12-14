import time

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from pharmacies.models import Pharmacy, Employee, Rating
from pharmacies.forms import PharmacyForm, CommentForm
from django.db.models import Q

def pharmacy(request, pk):
    pharmacy = Pharmacy.objects.get(pk=pk)
    rated_list = Rating.objects.filter(pharmacy = pharmacy)

    if rated_list:
        acc_rating = 0
        for rating in rated_list:
            acc_rating += rating.rating 
        rating = int(round(acc_rating / len(rated_list)))
    else:
        rating = None
    args = {'pharmacy': pharmacy, 'rating': rating}
    return render(request, 'pharmacies/pharmacy_profile.html', args)

def create_pharma(request):
    if request.method == 'POST':                # When we POST the form.
        form = PharmacyForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            name = form.cleaned_data.get('name')
            slug = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            return redirect ('home') 
    else:                                       
        form = PharmacyForm() 
    return render(request, 'pharmacies/create_pharmacy.html', {'form': form})

def add_comment_to_pharmacy(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            form.save(pk, user)
            return redirect('pharmacies:pharmacy', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'pharmacies/add_comment_to_pharmacy.html', {'form': form})

def add_rating_to_pharmacy(request, pk, new_rating):
    user = request.user
    pharmacy = Pharmacy.objects.get(pk=pk) 
    try:
        rating = Rating.objects.get(pharmacy = pharmacy, user=user)
        rating.rating = new_rating
    except Rating.DoesNotExist:
        rating = Rating(user=user, pharmacy=pharmacy, rating=new_rating)
    rating.save()

    return redirect('pharmacies:pharmacy', pk=pk)

def search(request):
    start = time.time()
    query = request.GET.get('q')
    results = []
    if query:
        results = Pharmacy.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    
    end = time.time()
    processing_time = format((end - start), '.4f')
    num_results = len(results)
    args = {'results': results, 'query': query, 'time': processing_time, 'num_results': num_results}
    return render(request, 'pharmacies/search.html', args)