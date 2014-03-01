from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import auth
from django.contrib import messages

from shoppingcart.models import UserProfile

def index(request):
    return render(request, 'shoppingcart/index.html',RequestContext(request))

# user management

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        print user
        print user.userprofile.store
        if user is not None and user.is_active and user.userprofile.store == request.store:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            # Show an error page
            messages.add_message(request, messages.INFO, 'Login Failed')
            return HttpResponseRedirect("/login")
    return render(request, 'shoppingcart/login.html', RequestContext(request))

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

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
        return HttpResponseRedirect('/')
    return render(request, 'shoppingcart/register.html', \
        RequestContext(request))
