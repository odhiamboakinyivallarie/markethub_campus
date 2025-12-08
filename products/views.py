

from django.shortcuts import render
from .models import Product

def homepage(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'products/home.html', {'products': products})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()
        return user


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Auto login after registration
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Change to your home URL name
    else:
        form = StudentRegistrationForm()

    return render(request, 'registration/register.html',{'form':form})

def products_list(request):
    products = Product.objects.all()
    return render(request, "products/products_list.html", {"products": products})

def home(request):
    products = Product.objects.all()  # gets all products from the database
    return render(request, 'products/home.html', {'products': products})

