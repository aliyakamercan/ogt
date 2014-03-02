from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from shoppingcart.models import UserProfile, Product, Order, OrderDetail
from shoppingcart.cart import Cart


def index(request):
    products = Product.objects.filter(store=request.store)
    return render(request, 'shoppingcart/index.html',RequestContext(request,\
        dict(products=products)))

# user management

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active and user.userprofile.store == request.store:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            next = request.GET.get('next', reverse('index'))
            return HttpResponseRedirect(next)
        else:
            # Show an error page
            messages.add_message(request, messages.INFO, 'Login Failed!')
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'shoppingcart/login.html', RequestContext(request))

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, 'Logged out. Please Visit again!')
    return HttpResponseRedirect(reverse('index'))

def register(request):
    print "asdasd"
    print request.POST
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print username
        print password
        user = User.objects.create_user(username, None, password)
        userprofile = UserProfile(user=user, store = request.store)
        userprofile.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'shoppingcart/register.html', \
        RequestContext(request))

# cart functionality

def add_to_cart(request):
    cart = Cart(request)
    try:
        pk = request.GET.get('product_id')
        print pk
        product = Product.objects.get(id=pk)
        print product
        cart.add(pk)
        messages.add_message(request, messages.INFO, '%s added to cart. Continue shopping or visit your cart to checkut' \
        % product.name)
    except:
        messages.add_message(request, messages.INFO, 'Ops something went wrong. Try again later pls')
    return HttpResponseRedirect(reverse('index'))

def cart(request):
    cart = Cart(request)
    context =  {
        'cart': cart.cart,
        'products': Product.objects.filter(pk__in=cart.cart.keys()),
        'sum': cart.total()
    }
    return render(request, 'shoppingcart/cart.html', \
        RequestContext(request, context))

def remove(request):
    pk = request.GET.get('pk')
    cart = Cart(request)
    cart.remove(pk)
    return HttpResponseRedirect(reverse('cart'))

def update(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        quantity = request.POST.get('quantity', '')
        cart = Cart(request)
        cart.update(pk, quantity)
        return HttpResponseRedirect(reverse('cart'))

@login_required(login_url='/login')
def checkout(request):
    if request.method == 'POST':
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total=cart.total())
        for key in cart.cart:
            od = OrderDetail.objects.create(order=order, \
                product=Product.objects.get(id=key), quantity=cart.cart[key])
            od.save()
        context = {}
        return render(request, 'shoppingcart/checkout.html', \
            RequestContext(request, context))