from django.shortcuts import render, redirect
from pharmacies.models import Pharmacy
from pharmacies.forms import PharmacyForm

def pharmacy_detail(request, pharmacy_id, slug):
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id, slug=slug, available=True)
    args = {'pharmacy': pharmacy,}
    return render(request, 'pharmacy/detail.html', args)

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
