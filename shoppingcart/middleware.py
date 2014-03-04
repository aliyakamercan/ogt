# mostly taken from https://github.com/tkaemming/django-subdomains

import operator
import logging
import re

from django.contrib.sites.models import Site
from django.conf import settings
from django.shortcuts import render

from shoppingcart.models import Store

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

def current_site_domain():
    domain = Site.objects.get_current().domain

    prefix = 'www.'
    if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
            and domain.startswith(prefix):
        domain = domain.replace(prefix, '', 1)

    return domain


class SubdomainProcessor(object):
    """
    A middleware class that adds a ``subdomain`` attribute to the current request.
    """
    def get_domain_for_request(self, request):
        """
        Returns the domain that will be used to identify the subdomain part
        for this request.
        """
        return current_site_domain()

    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.
        """
        domain, host = map(lower,
            (self.get_domain_for_request(request), request.get_host()))
        pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
        matches = re.match(pattern, host)
        request.store = None
        if matches:
            subdomain = matches.group('subdomain')
            request.store = Store.objects.filter(sub_domain = subdomain).first()
        if not request.store:
            if  "admin" not in request.path: #not admin page req
                stores = Store.objects.all()
                return render(request, "shoppingcart/storenotfound.html", dict(stores=stores))