

from django.shortcuts import render
from .models import Product

def homepage(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'products/home.html', {'products': products})



from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product, Category
from .forms import ProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1

    item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    total = cart.total_price()

    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()

    if not items:
        return redirect('view_cart')

    total = cart.total_price()

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def confirm_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()

    if not items:
        return redirect('view_cart')

    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price(),
        status="Pending"
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # clear cart
    cart.cartitem_set.all().delete()

    return render(request, 'order_success.html', {
        'order': order
})

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
    categories = Category.objects.all()

    # Search filter
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__id=category_filter)

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
})
def home(request):
    products = Product.objects.all()  # gets all products from the database
    return render(request, 'products/home.html', {'products': products})
def sell_item(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()

    return render(request, 'products/sell_item.html',{'form': form})

