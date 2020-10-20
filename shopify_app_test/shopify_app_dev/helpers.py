from functools import wraps
from typing import List
import logging
import re
import hmac
import base64
import hashlib
from django.http import HttpRequest,HttpResponse,Http404,request
from .Shopify_client import ShopifyStoreClient
from .config import SHOPIFY_API_KEY,SERVER_HOST_NAME,APP_NAME,SHOPIFY_API_SECRET_KEY
import urllib
import shopify
from .models import StoreToken
#SERVER_BASE_URL = f"https://{SERVER_HOST_NAME}"
#INSTALL_REDIRECT_URL = f"{SERVER_BASE_URL}/app_installed"
#WEBHOOK_APP_UNINSTALL_URL = f"https://{SERVER_HOST_NAME}/app_uninstall"
API_VERSION = '2020-10'
STORE_CLIENT = None
def isAppInstalled():
    global STORE_CLIENT
    if len(StoreToken.objects.all())>0:
        obj = StoreToken.objects.get(pk=1)
        STORE_CLIENT=ShopifyStoreClient(SHOPIFY_API_KEY,SHOPIFY_API_SECRET_KEY,obj.store_url,API_VERSION,obj.token)
        return True
    return False
def generate_install_redirect_url(shop_url:str,scopes:List,nonce:str, access_mode:List):
    global STORE_CLIENT
    shopify.Session.setup(api_key=SHOPIFY_API_KEY, secret=SHOPIFY_API_SECRET_KEY)
    newSession = shopify.Session(shop_url,API_VERSION)
    STORE_CLIENT=ShopifyStoreClient(SHOPIFY_API_KEY,SHOPIFY_API_SECRET_KEY,shop_url,API_VERSION)
    INSTALL_REDIRECT_URL = f"https://{SERVER_HOST_NAME}/app_installed"
    auth_url = newSession.create_permission_url(scopes,INSTALL_REDIRECT_URL,nonce)
    auth_url = urllib.parse.unquote(auth_url)
    print("auth_url",auth_url)
    shopify.ShopifyResource.clear_session()
    return auth_url

def generate_post_install_redirect_url(request_params:dict):
    #Include the server host name here with the redirect to read the data
    global STORE_CLIENT
    print('request_params',request_params)
    shopify.Session.setup(api_key=SHOPIFY_API_KEY, secret=SHOPIFY_API_SECRET_KEY)
    session = shopify.Session(STORE_CLIENT.shop_url, API_VERSION)
    access_token = session.request_token(request_params)
    print(access_token)
    STORE_CLIENT.putAccessCode(access_token)
    shopify.ShopifyResource.clear_session()
    return True

def get_shop_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getStore()
    return "Error"

def get_product_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getProduct()
    return "Error"

def get_customer_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getCustomer()
    return "Error"

def get_discountCode_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getDiscountCode()
    return "Error"

def get_marketingEvents_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getMarketingEvents()
    return "Error"

def get_order_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getOrder()
    return "Error"

def get_collect_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getCollect()
    return "Error"

def get_collection_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getCollection()
    return "Error"

def get_productImage_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.getProductImages()
    return "Error"

def get_productVariants_details():
    if isAppInstalled():
        print("Success!!")
        return STORE_CLIENT.productVariant()
    return "Error"

"""
MarketingEvents
Customer-->Address
Collect-->Collection-->CollectionImage
Collect-->Product-->ProductImage-->ProductVariant
PriceRule--> PriceRuleSavedSearch --->PrerequisiteCustomer-->PriceRuleEntity-->PrerequisiteProducts-->PriceRuleProduct-->PrerequisiteVariants-->PriceProductVariant-->DiscountCode
AbandonCart-->AbandonCartLineItem
Order  -->OrderLocation-->orderNote-->orderTag-->OrderLineItem
ClientOrder
OrderdiscountCode
"""
   
    

def verify_hmac(data:bytes,orig_hmac:str)->bool:
    new_hmac= hmac.new(
        SHOPIFY_API_SECRET_KEY.encode('utf-8'),
        data,
        hashlib.sha256
    )
    return new_hmac.hexdigest() == orig_hmac

def is_valid_shop(shop:str)-> bool:
    shopname_regex = r'[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com[\/]?'
    return re.match(shopname_regex,shop)

