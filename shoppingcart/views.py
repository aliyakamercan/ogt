from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import select_template
from django.views.decorators.http import require_http_methods

from shoppingcart.models import UserProfile, Product, Order, OrderDetail
from shoppingcart.cart import Cart


def index(request):
    context = {
        'products' : Product.objects.filter(store=request.store)
    }
    t = select_template(['shoppingcart/' + request.store.sub_domain + \
        '/index.html', 'shoppingcart/index.html'])
    return HttpResponse(t.render(RequestContext(request, context)))

# user management

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.POST.get('next', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active and user.userprofile.store == request.store:
            auth.login(request, user)
            return HttpResponseRedirect(next)
        else:
            # Show an error page
            messages.add_message(request, messages.INFO, 'Login Failed!')
            return HttpResponseRedirect(reverse('login'))
    t = select_template(['shoppingcart/' + request.store.sub_domain + \
        '/login.html', 'shoppingcart/login.html'])
    context = {
        'next' : request.GET.get('next', reverse('index'))
    }
    return HttpResponse(t.render(RequestContext(request, context)))

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, 'Logged out. Please Visit again!')
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.POST.get('next', '/')
        try:
            user = User.objects.create_user(username, None, password)
        except:
            messages.add_message(request, messages.INFO, 'Username taken')
        else:
            userprofile = UserProfile(user=user, store = request.store)
            userprofile.save()
            return HttpResponseRedirect("%s?next=%s" % (reverse('login'), next))

    t = select_template(['shoppingcart/' + request.store.sub_domain + \
        '/register.html', 'shoppingcart/register.html'])
    context = {
        'next' : request.GET.get('next', request.POST.get('next', reverse('index')))
    }
    return HttpResponse(t.render(RequestContext(request, context)))

# cart functionality

@require_http_methods(["GET", "POST"])
def cart(request, pk = None, quantity = None):
    cart = Cart(request)
    if request.method == "GET":
        context =  {
            'cart': cart.cart,
            'products': Product.objects.filter(pk__in=cart.cart.keys()),
            'sum': cart.total()
        }
        t = select_template(['shoppingcart/' + request.store.sub_domain + \
            '/cart.html', 'shoppingcart/cart.html'])
        return HttpResponse(t.render(RequestContext(request, context)))
    elif request.method == "POST" and pk:
        quantity = request.POST.get('quantity')
        if quantity:
            cart.update(pk, quantity)
            return HttpResponseRedirect(reverse('cart'))
        else:
            product = Product.objects.get(id=pk)
            cart.add(pk)
            messages.add_message(request, messages.INFO, '%s added to cart. Continue shopping or visit your cart to checkut' \
        % product.name)
            return HttpResponseRedirect(reverse('index'))


# checkout process

@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        address = request.POST.get('address')
        order = Order.objects.create(user=request.user, total=cart.total(), address=address)
        for key in cart.cart:
            od = OrderDetail.objects.create(order=order, \
                product=Product.objects.get(id=key), quantity=cart.cart[key])
            od.save()
        t = select_template(['shoppingcart/' + request.store.sub_domain + \
            '/order_complete.html', 'shoppingcart/order_complete.html'])
        context = {}
        cart.clear()
        return HttpResponse(t.render(RequestContext(request, context)))
    elif request.method == 'GET':
        context =  {
                'cart': cart.cart,
                'products': Product.objects.filter(pk__in=cart.cart.keys()),
                'sum': cart.total()
            }
        t = select_template(['shoppingcart/' + request.store.sub_domain + \
                '/checkout.html', 'shoppingcart/checkout.html'])
        return HttpResponse(t.render(RequestContext(request, context)))

# user orders

@login_required(login_url='/login')
@require_http_methods(["GET"])
def orders(request):
    orders = request.user.order_set.all()
    context =  {
            'orders': orders
        }
    t = select_template(['shoppingcart/' + request.store.sub_domain + \
            '/orders.html', 'shoppingcart/orders.html'])
    return HttpResponse(t.render(RequestContext(request, context)))

@login_required(login_url='/login')
@require_http_methods(["GET"])
def order_detail(request, id):
    order_details = OrderDetail.objects.filter(order=id)
    context =  {
            'order_details': order_details
        }
    t = select_template(['shoppingcart/' + request.store.sub_domain + \
            '/order_detail.html', 'shoppingcart/order_detail.html'])
    return HttpResponse(t.render(RequestContext(request, context)))