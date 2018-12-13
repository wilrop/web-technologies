from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from pharmacies.models import Pharmacy, Employee
from pharmacies.forms import PharmacyForm
from django.db.models import Q

def pharmacy_detail(request, pharmacy_id, slug):
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id, slug=slug)
    entries = Employee.objects.filter(pharmacy=pharmacy.id)
    args = {'pharmacy': pharmacy, 'entries': entries}
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

def search(request):
    query = request.GET.get('q')

    if query:
        results = Pharmacy.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
        args = {'results': results}
    
    return render(request, 'pharmacies/search.html', args)

