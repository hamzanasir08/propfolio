from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser  # Assuming your model is in the same app
from dashboard import views
def home(request):
  return render(request,'home.html')

def signup(request):
  if request.method == 'POST':
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    phone_number = request.POST.get('phone')
    cnic = request.POST.get('cnic')

    # Validate data (optional)
    # ... add validation logic here ...

    user = CustomUser.objects.create_user(
      username = email,
      email=email,
      password=password,
      first_name=first_name,
      last_name=last_name,
      cnic=cnic,
      phone_number=phone_number
    )

    if user is not None:
      login(request, user)  # Login the user
      return redirect('property_list')  # Redirect to the home page after successful login
    else:
      # Handle user creation error (e.g., display message)
      print('User creation failed. Please try again.')

  return render(request, 'registration/checkregister.html')



def logined(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Authenticate the user based on email (as you're using email as username)
    user = authenticate(email=email, password=password)

    if user is not None:
      login(request, user)  # Login the user if credentials are valid
      return redirect('property_list')  # Redirect to the home page after successful login
    else:
      # Handle unsuccessful login attempt (e.g., display error message)
      print('Invalid login credentials. Please try again.')

  return render(request, 'registration/checklogin.html')