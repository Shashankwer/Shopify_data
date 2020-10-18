import json
from typing import List
import logging
import requests
from requests.exceptions import HTTPError
import shopify
from .models import StoreToken
class ShopifyStoreClient():
    def __init__(self,api_key,api_secret_key,shop_url,api_version,access_token=''):
        self.api_key = api_key
        self.secret_key = api_secret_key
        self.shop_url = shop_url
        self.access_token = access_token
        self.api_version = api_version
    
    def putAccessCode(self,code):
        obj = StoreToken(token = code, store_url=self.shop_url)
        obj.save()
        self.access_token = code
    
    def getStore(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current()
        shopify.ShopifyResource.clear_session()
        return shop




