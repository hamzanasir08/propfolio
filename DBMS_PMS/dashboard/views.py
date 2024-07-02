from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Image, City, Town, Appointment
from userReg.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from userReg import views
from datetime import datetime, timedelta

# Create your views here.


def dashboard_view(request):
    return render(request,'dashboard.html')

def homeview(request):
    return render(request,'home.html')

def contactview(request):
    return render(request,'contact.html')

def aboutview(request):
    return render(request,'about.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('property_list') 

@login_required(login_url='/register/logined/')
def submit_property(request):
    if request.method == 'POST':
        facing = request.POST['facing']
        price = request.POST['price']
        number_of_bedrooms = request.POST['bedrooms']
        number_of_bathrooms = request.POST['bathrooms']
        sale_type = request.POST['sale_type']
        address = request.POST['address']
        city_id = request.POST['city']
        town_id = request.POST['town']
        description = request.POST['description']
        
        city = City.objects.get(pk=city_id)
        town = Town.objects.get(pk=town_id)
        user = request.user  # Assuming user is logged in

        property = Property.objects.create(
            facing=facing,
            price=price,
            number_of_bedrooms=number_of_bedrooms,
            number_of_bathrooms=number_of_bathrooms,
            sale_type=sale_type,
            address=address,
            city=city,
            town=town,
            user=user,
            description=description
        )

        for image in request.FILES.getlist('images'):
            img = Image.objects.create(images=image)
            property.images.add(img)

        property.save()

        return redirect('dashboard_view')  # Redirect to a property list page or success page

    cities = City.objects.all()
    return render(request, 'addProp.html', {'cities': cities})
  
def get_towns(request):
    city_id = request.GET.get('city_id')
    towns = list(Town.objects.filter(city_id=city_id).values('townID', 'town_name'))
    return JsonResponse(towns, safe=False)

# it will display all properties in db
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})


def property_detail(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    return render(request, 'property_detail.html', {'property': property})


# it will display properties listed by logined user
@login_required(login_url='/register/logined/')
def user_properties(request):
    user = request.user
    properties = Property.objects.filter(user=user)
    return render(request, 'property_list.html', {'properties': properties})

@login_required
def prop_delete(request, prop_id):
    prop = get_object_or_404(Property, pk = prop_id, user = request.user)
    if request.method == 'POST':
        prop.delete()
        return redirect(user_properties)
    return render(request, 'prop_delete_confirmation.html',{'prop': prop})


@login_required
def edit_property(request, prop_id):
    prop = get_object_or_404(Property, pk=prop_id, user=request.user)
    
    if request.method == 'POST':
        prop.facing = request.POST['facing']
        prop.price = request.POST['price']
        prop.number_of_bedrooms = request.POST['bedrooms']
        prop.number_of_bathrooms = request.POST['bathrooms']
        prop.sale_type = request.POST['sale_type']
        prop.address = request.POST['address']
        prop.city = City.objects.get(pk=request.POST['city'])
        prop.town = Town.objects.get(pk=request.POST['town'])
        prop.description = request.POST['description']

        # Handle images
        if 'images' in request.FILES:
            prop.images.clear()  # Remove existing images if new ones are uploaded
            for image in request.FILES.getlist('images'):
                img = Image.objects.create(images=image)
                prop.images.add(img)

        prop.save()
        return redirect('user_properties')

    cities = City.objects.all()
    towns = Town.objects.filter(city=prop.city)

    context = {
        'prop': prop,
        'cities': cities,
        'towns': towns
    }
    return render(request, 'edit_property.html', context)












def book_appointment(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        appointment_date_and_time = request.POST.get('appointment_date_and_time')
        visiting_user_id = request.POST.get('visiting_user')
        prop_id = request.POST.get('propID')
        user_id = request.POST.get('userID')

        visiting_user = CustomUser.objects.get(id=visiting_user_id)
        prop = Property.objects.get(id=prop_id)
        user = CustomUser.objects.get(id=user_id)

        # Parse the appointment date and time
        appointment_datetime = datetime.strptime(appointment_date_and_time, '%Y-%m-%dT%H:%M')
        start_time = appointment_datetime
        end_time = appointment_datetime + timedelta(hours=1)

        # Check for existing appointments within the same time range
        if Appointment.objects.filter(propID=prop, appointment_date_and_time__range=(start_time, end_time)).exists():
            messages.error(request, 'This time slot is already booked. Please choose another time.')
            return render(request, 'book_appointment.html', {'property': property})

        # No conflicts, save the appointment
        appointment = Appointment(
            appointment_date_and_time=appointment_date_and_time,
            visiting_user=visiting_user,
            propID=prop,
            userID=user
        )
        appointment.save()

        return redirect('appointment_success')  # Redirect to a success page or some other page

    return render(request, 'book_appointment.html', {'property': property})

@login_required
def appointment_success(request):
    return render(request, 'appointment_success.html')




@login_required
def view_appointments(request):
    # Appointments for properties posted by the logged-in user
    properties_posted_by_user = Property.objects.filter(user=request.user)
    appointments_for_user_properties = Appointment.objects.filter(propID__in=properties_posted_by_user)

    # Appointments booked by the logged-in user to visit other properties
    appointments_booked_by_user = Appointment.objects.filter(visiting_user=request.user)

    context = {
        'appointments_for_user_properties': appointments_for_user_properties,
        'appointments_booked_by_user': appointments_booked_by_user,
    }

    return render(request, 'view_appointments.html', context)


# @login_required
# def cancel_appointment(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     # Only allow the user who booked the appointment to cancel it
#     if appointment.visiting_user == request.user:
#         appointment.delete()
#         messages.success(request, 'Appointment cancelled successfully.')
#         print('Appointment cancelled successfully.')
#     else:
#         messages.error(request, 'You do not have permission to cancel this appointment.')
#         print('You do not have permission to cancel this appointment.')

#     return redirect('view_appointments')