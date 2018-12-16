import time

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
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

    form = CommentForm
    args = {'pharmacy': pharmacy, 'rating': rating, 'form': form}
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
            return redirect('phone_verification') 
    else:                                       
        form = PharmacyForm() 
    return render(request, 'pharmacies/create_pharmacy.html', {'form': form})

def add_comment_to_pharmacy(request):
    user = request.user
    author = user.username
    pharmacy = request.POST.get('pharmacy', None)
    text = request.POST.get('text', None)

    form = CommentForm({'text': text})
    if form.is_valid():
        valid = True
        comment = form.save(pharmacy, user)
        date = comment.created_date
    else:
        valid = False
        date = None

    data = {
        'valid': valid,
        'author': author,
        'text': text,
        'date': date,
    }
    return JsonResponse(data)

def add_rating_to_pharmacy(request):
    pk = request.GET.get('pk', None)
    new_rating = int(request.GET.get('new_rating', None))
    pharmacy = Pharmacy.objects.get(pk=pk)
    user = request.user

    rated_list = Rating.objects.filter(pharmacy = pharmacy)
    acc_rating = 0

    if rated_list:      
        for rating in rated_list:
            acc_rating += rating.rating 
        old_rating = int(round(acc_rating / len(rated_list)))
    else:
        old_rating = 1

    try:
        rating = Rating.objects.get(pharmacy = pharmacy, user=user)
        previous_rating = rating.rating
        rating.rating = new_rating
        new_rating = int(round((acc_rating - previous_rating + new_rating)/len(rated_list)))
    except Rating.DoesNotExist:
        rating = Rating(user=user, pharmacy=pharmacy, rating=new_rating)
        new_rating = int(round((acc_rating + new_rating)/(len(rated_list) + 1)))
    rating.save()

    data = {
        'old_rating': old_rating ,
        'new_rating': new_rating
    }
    return JsonResponse(data)


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