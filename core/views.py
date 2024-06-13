from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Product
from django.contrib.auth.decorators import login_required 



# Create your views here.
def home(request):
    count = User.objects.count()
    products = Product.objects.all()[0:8]
    return render(request, 'home.html', {
        'count' : count,
        'products': products
    })
    
def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form' : form
    })
    
