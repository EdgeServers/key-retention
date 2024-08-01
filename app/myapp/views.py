from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ArrivalForm, DepartureForm
from .models import Driver, KeyHanger
from datetime import datetime

def arrival(request):
    if request.method == 'POST':
        form = ArrivalForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.arrival_time = datetime.now()
            driver.save()
            key_hanger = driver.key_hanger_number
            key_hanger.is_available = False
            key_hanger.save()
            return render(request, 'thank_you.html', {
                'message': 'Arrival recorded successfully!',
                'key_hanger_number': key_hanger.hanger_number
            })
    else:
        form = ArrivalForm()
    return render(request, 'arrival.html', {'form': form})

def departure(request):
    if request.method == 'POST':
        form = DepartureForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            key_hanger_number = form.cleaned_data['key_hanger_number']

            try:
                # Convert the key_hanger_number to an integer
                key_hanger_number = int(key_hanger_number)
                key_hanger = KeyHanger.objects.get(hanger_number=key_hanger_number)
            except (ValueError, KeyHanger.DoesNotExist):
                form.add_error('key_hanger_number', 'Invalid key hanger number.')
                return render(request, 'departure.html', {'form': form})

            driver.departure_time = datetime.now()
            driver.save()
            key_hanger.is_available = True
            key_hanger.save()
            return render(request, 'thank_you_depart.html', {
                'message': 'Departure recorded successfully!',
                'key_hanger_number': key_hanger_number
            })
    else:
        form = DepartureForm()
        driver_id = request.GET.get('driver_id')
        if driver_id:
            driver = get_object_or_404(Driver, id=driver_id)
            # Ensure the key_hanger_number is set correctly
            form.fields['key_hanger_number'].initial = driver.key_hanger_number.hanger_number
    return render(request, 'departure.html', {'form': form})



def get_key_hanger_number(request):
    driver_id = request.GET.get('driver_id')
    
    if not driver_id:
        return JsonResponse({'error': 'Driver ID not provided'}, status=400)
    try:
        driver = Driver.objects.get(id=driver_id)
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Driver not found'}, status=404)

    # Check if driver has an associated KeyHanger
    if driver.key_hanger_number:
        key_hanger_number = driver.key_hanger_number.hanger_number
    else:
        key_hanger_number = ''  # or return an appropriate error message if needed

    return JsonResponse({'key_hanger_number': key_hanger_number})

def active_drivers(request):
    drivers = Driver.objects.filter(key_hanger_number__isnull=False, departure_time__isnull=True)
    return render(request, 'active_drivers.html', {'drivers': drivers})



def get_active_drivers(request):
    drivers = Driver.objects.filter(departure_time__isnull=True)
    data = list(drivers.values('name', 'truck_rego_number', 'key_hanger_number__hanger_number', 'parking_location__name', 'arrival_time'))
    return JsonResponse(data, safe=False)


def welcome(request):
    return render(request, 'index.html')
