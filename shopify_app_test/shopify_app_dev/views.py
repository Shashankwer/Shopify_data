from django.shortcuts import render,redirect
import uuid
import os
import json
import logging
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect,Http404
from . import helpers

# Create your views here.
SHOPIFY_CLIENT= None
ACCESS_TOKEN = None
NOUNCE = None 
ACCESS_MODE = [] #defaults to offline access mode if left blank or omitted. 
SCOPES = ['read_products','read_orders','read_all_orders']
def validate_url(dic)->bool:
    hmac = dic.get('hmac')
    sorted(dic)
    data = '&'.join([f"{key}={value}" for key,value in dic.items() if key!='hmac']).encode('utf-8')
    if not helpers.verify_hmac(data,hmac):
        logging.error(f"HMAC could not be verified:\n\thmac {hmac}\n\tdata {data}")
        raise Http404("HMAC could not be verified")
    shop = dic.get('shop')
    if shop and not helpers.is_valid_shop(shop):
        logging.error(f"invalid shop name received")
        raise Http404("Invalid shop name")
    return True

def app_launched(request):
    print(helpers.isAppInstalled())
    if helpers.isAppInstalled():
        return redirect('../app_installed/gather_data/')
    validate_url(request.GET)
    shop = request.GET.get('shop')
    print(shop)
    global ACCESS_TOKEN, NONCE
    NONCE  = uuid.uuid4().hex
    redirect_url = helpers.generate_install_redirect_url(shop_url=shop,scopes=SCOPES,nonce=NONCE,access_mode=ACCESS_MODE)
    print(redirect_url)
    return HttpResponseRedirect(redirect_url)

def app_installed(requests):
    validate_url(requests.GET)
    redirects = helpers.generate_post_install_redirect_url(requests.GET)
    print("redirects",redirects)
    if redirects:
        print("Hello World!!!")
        return redirect('gather_data/')
    return Http404()    
    
def gather_data(request):
    shop = helpers.get_shop_details()
    return HttpResponse(f'<html><p>{shop.address1}</p><p>{shop.address2}</p><p>{shop.checkout_api_supported}</p><p>{shop.enabled_presentment_currencies[0]}</p><p>{shop.setup_required}</p><p>{shop.cookie_consent_level}</p></html>')
