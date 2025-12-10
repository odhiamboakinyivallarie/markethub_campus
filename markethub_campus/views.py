from django.shortcuts import render

def home(request):
    return render(request, 'products/pythhome.html')

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request,'products/contact.html')