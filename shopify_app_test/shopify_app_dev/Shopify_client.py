import json
from typing import List
import logging
import requests
from requests.exceptions import HTTPError
import shopify
from .models import StoreToken
from django.utils import timezone
from .models import PriceRule,PriceRuleSavedSearch,DiscountCode,MarketingEvents,Address,Customer,CustomerAddress,PrerequisiteCustomer,AbandonCart,Order,ClientOrder,OrderdiscountCode,Collection,PriceRuleEntity,Product,PrerequisiteProducts,PriceRuleProduct,ProductImage,Collect,CollectionImage,OrderLineItem,AbandonCartLineItem,PriceProductVariant,PrerequisiteVariants,OrderLineItem,orderNote,orderTag,ProductVariant,PrerequisiteVariants,OrderLocation


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

    def getProduct(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        products = shopify.Product.current()
        shopify.ShopifyResource.clear_session()
        return products
    
    def getCustomer(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        customers = shopify.Customer.current()
        shopify.ShopifyResource.clear_session()
        return customers

    def getDiscountCode(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        discountCode = shopify.DiscountCode.current()
        shopify.ShopifyResource.clear_session()
        return discountCode

    def getMarketingEvents(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        marketingEvents = shopify.MarketingEvent.current()
        shopify.ShopifyResource.clear_session()
        return marketingEvents

    def getOrder(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        order = shopify.Order.current()
        shopify.ShopifyResource.clear_session()
        return order

    def getCollect(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        collect = shopify.Collect.current()
        shopify.ShopifyResource.clear_session()
        return collect

    def getCollection(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        collection = shopify.CollectionListing.current()
        shopify.ShopifyResource.clear_session()
        return collection        

    def getProductImages(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        productImage = shopify.ProductImage.current()
        shopify.ShopifyResource.clear_session()
        return productImages

    def getProductVariants(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        productVariant = shopify.Variant.current()
        shopify.ShopifyResource.clear_session()
        return productVariant
    
    
    
    
    def loadPriceRule(self,id,allocation_method = '',created_at=timezone.now,updated_at = timezone.now,customer_selection = '',ends_at = timezone.now,once_per_customer = True,prerequisite_quantity_range = 1,prerequisite_shipping_price_range = '',prerequisite_subtotal_range = 0.0,prerequisite_purchase = 0.0,starts_at = timezone.now,target_selection = '',target_type = '',title= '',usage_limit = 10):
        obj = PriceRule(allocation_method,created_at,updated_at,customer_selection,ends_at,id,once_per_customer,prerequisite_purchase,prerequisite_quantity_range,prerequisite_shipping_price_range,prerequisite_subtotal_range,prerequisite_purchase,starts_at,target_selection,target_type,title,usage_limit)
        obj.save()
        return True

    def loadPriceRuleSavedSearch(self,price_rule_id,saved_search=''):
        price_obj  =  PriceRule.objects.filter(id=price_rule_id)
        obj = PriceRuleSavedSearch(price_rule_id = price_obj,saved_search = saved_search)
        obj.save()

    def loadDiscountCode(self,id, price_rule_id,code='',useage_count='',created_at= timezone.now,updated_at = timezone.now):
        price_obj  =  PriceRule.objects.filter(id=price_rule_id)
        obj = DiscountCode(id= id,price_rule_id= price_obj,code= code,useage_count = useage_count,created_at= created_at,updated_at= updated_at)
        obj.save()

    def loadMarketingEvents(self,remote_id,event_type = '',marketing_channel = '',paid = '',referrring_domain = '',budget = 0,currency = '',budget_type = '',started_at = timezone.now,scheduled_end_at = timezone.now,ended_at = timezone.now,utm_campaign = '',utm_source = '',utm_medium = '',description = '',manage_url = '',preview_url = '',marketing_source = ''):
        obj = MarketingEvents(remote_id = remote_id,event_id =event_type,marketing_channel= marketing_channel,paid= paid,referring_domain = referrring_domain,budget= budget,currency= currency,budget_type= budget_type,started_at= started_at,scehduled_end_at = scheduled_end_at,ended_at = ended_at,utm_campaign= utm_campaign,utm_source= utm_source,utm_medium= utm_medium,decription= description,manage_url= manage_url,preview_url= preview_url,marketing_source= marketing_source) 
        obj.save()       

    def loadAddress(self,address_id,address_type = '',company =  '',address1 =  '',address2 =  '',city =  '',latitude = '',longitutde  = '',country =  '',zipcode =  '',default = False,province_code = '',country_code = '',first_name = '',last_name = '',billing_Address_type = ''):
        obj = Address(default, address_type, address_id, company, address1, address2, city, latitude, longitutde, country, zipcode, province_code, country_code, first_name, last_name, billing_Address_type)
        obj.save()
    
    def loadCustomer(self,id,last_order_id ='',email = '',accept_marketing = False,created_at = timezone.now,updated_at = timezone.now,first_name = '',last_name = '',order_count = 0,state = '',total_spent = 0,multi_pass_identifier = '',tax_exempt=False,tags = '',last_order_name = '',currency = '',marketing_optin_level = ''):
        obj = Customer(created_at, updated_at, id, currency, first_name, last_name, email, accept_marketing, order_count, state, total_spent, last_order_id, multi_pass_identifier, tax_exempt, tags, last_order_name, marketing_optin_level)
        obj.save()

    def loadCustomerAddress(self,customer_id,address_id,default = False):
        customer_obj = Customer.objects.filter(id=customer_id)
        address_obj = Address.objects.filter(id = address_id)
        obj = CustomerAddress(customer_id=customer_obj,address_id=address_obj,default=default)
        obj.save()

    def loadPrerequisiteCustomer(self,price_rule_id,customer_id):
        price_rule_obj= PriceRule.objects.filter(id = price_rule_id)
        customer_obj = Customer.objects.filter(id = customer_id)
        obj = PrerequisiteCustomer(price_rule_obj, customer_obj)
        obj.save()
    
    def loadAbandonCart(self,id,customer_id,user_id='',device_id='',buyer_accepts_marketing=False,cart_token = '',completed_at = timezone.now,created_at = timezone.now,customer_locale = '',gateway  = '',landing_site='',location = '',note = '',currency_code = '',referring_site = '',source_name = '',subtotal_price = 0.0,tokens = '',total_discount = 0.0,total_price = 0.0,total_weight = 0.0,updated_at = timezone.now):
         customer_obj = Customer.objects.filter(id = customer_id)
         obj = AbandonCart(created_at, updated_at, id, customer_obj, buyer_accepts_marketing, cart_token, completed_at, customer_locale, device_id, gateway, landing_site, location, note, currency_code, referring_site, source_name, subtotal_price, tokens, total_discount, total_price, total_weight, user_id)
         obj.save()

    def loadOrder(self,id,customer_id,app_id='',browser_ip = '',buyer_accepts_marketing = False,cancel_reason = '',cancelled_at = timezone.now,cart_token = '',checkout_id='',closed_at = timezone.now,created_at = timezone.now,currency = '',customer_locale = '',order_email = '',order_financial_status = '',fullfillment_status = '',gateway = '',landing_site = '',landing_site_ref = ''    ,name = '',notes = '',number = 0,order_number= 0,payment_gateway = '',presenment_currency = '',referring_site = '',source_name = '',total_discount = 0.0,total_line_item_price = 0.0,total_price = 0.0,total_line_tax = 0.0,total_tip = 0.0,user_id='',update_at = timezone.now,total_weight = ''):
        customer_obj = Customer.objects.filter(id = customer_id)
        obj = Order(created_at, id, currency, customer_obj, buyer_accepts_marketing, cart_token, customer_locale, gateway, landing_site, referring_site, source_name, total_discount, total_price, total_weight, user_id, app_id, browser_ip, cancel_reason, cancelled_at, checkout_id, closed_at, order_email, order_financial_status, fullfillment_status, landing_site_ref, name, notes, number, order_number, payment_gateway, presenment_currency, total_line_item_price, total_line_tax, total_tip, update_at)
        obj.save()
    
    def loadClientOrder(self,order_id,accept_language = '',browser_height = '',browser_width = '',session_hash = '',user_hash = ''):
        order_obj = Order.objects.filter(id = order_id)
        obj = ClientOrder(order_obj, accept_language, browser_height, browser_width, session_hash, user_hash)
        obj.save()

    def loadOrderdiscountCode(self,discount_code,order_id=None,abandoncart_id=None,discount_price = '',discount_type  = ''):
        discount_obj = DiscountCode.objects.filter(id =discount_code)
        if order_id is not None:
            order_obj = Order.objects.filter(id = order_id)
            obj = OrderdiscountCode(order_id = order_obj, abandoncart_id=None, discount_codes=discount_obj, discount_price='', discount_type='')
            obj.save()
        elif abandoncart_id is not None:
            abandon_obj = AbandonCart.objects.filter(id = order_id)
            obj = OrderdiscountCode(order_id = None, abandoncart_id=abandon_obj, discount_codes=discount_obj, discount_price='', discount_type='')
            obj.save()

    def loadCollection(self,id ,body_html='',handle = '',published_at = timezone.now,published_scope = '',sort_order = '',title = '',update_at = timezone.now):
        obj = Collection(id, title, update_at, body_html, handle, published_at, published_scope, sort_order)
        obj.save()
    
    def loadPriceRuleEntity(self,price_rule_id,collection_id):
        price_rule_obj = PriceRule.objects.filter(id = price_rule_id)
        collection_obj = Collection.objects.filter(id = collection_id)
        obj = loadPriceRule(price_rule_obj,collection_obj)
        obj.save()

    def loadProduct(self,id ,body_html='',handle = '',option_1='',option_2= '',option_3 = '',product_type = '',published_scope = '',status = '',published_date = timezone.now,update_at = timezone.now,tags = '',template_suffix = '',title = '',vendor = ''):
        obj = Product(id, title, tags, update_at, body_html, handle, published_scope, option_1, option_2, option_3, product_type, status, published_date, template_suffix, vendor)
        obj.save()

    def loadPrerequisiteProducts(self,pricerule_id,product_id):
        pricerule_obj = PriceRule.objects.filter(id = pricerule_id)
        product_obj = Product.objects.filter(id = product_id)
        obj = PrerequisiteProducts(pricerule_id=pricerule_obj,product_id=product_obj)
        obj.save()    

    def loadPriceRuleProduct(self,price_rule_id,product_id):
        pricerule_obj = PriceRule.objects.filter(id = pricerule_id)
        product_obj = Product.objects.filter(id = product_id)
        obj = PriceRuleProduct(price_rule_id=pricerule_obj,product_id=product_obj)
        obj.save()    

    def loadProductImage(self,product_id,id,position = -1,src = '',width = 0,height = 0,update_at = timezone.now):
        product_obj = Product.objects.filter(id = product_id)
        obj = ProductImage(id, update_at, product_obj, position, src, width, height)
        obj.save()

    def loadCollect(self,collection_id,product_id,created_at = timezone.now,position = -1,updated_at = timezone.now):
        product_obj = Product.objects.filter(id = product_id)
        collection_obj = Collection.objects.filter(id = collection_id)
        obj = Collect(created_at, updated_at, collection_obj, product_obj, position)
        obj.save()
    
    def loadCollectionImage(self,collection_id,src = '',alt = '',created_at = timezone.now,width = 0,height = 0):
        collection_obj = Collection.objects.filter(id = collection_id)
        obj = CollectionImage(created_at, collection_obj, src, width, height, alt)
        obj.save()

    def loadOrderLineItem(self,id,order_id,product_id,variant_id,fullfilment_quantity='',fullfilment_service = '',fullfilment_status = '',vendor = '',name = '',gift_card = '',properties = '',taxable = False,tip_payment_gateway = '',tip_payment_method = '',total_discount_amount = 0.0,properties=''):
        product_obj = Product.objects.filter(id=product_id)
        product_variant_obj = ProductImage.objects.filter(id=variant_id)
        order_obj = Order.objects.filter(id=order_id)
        obj = OrderLineItem(id=id, name=name, order_id=order_obj, vendor=vendor, product_id=product_obj, taxable=taxable, variant_id=product_variant_obj, fullfilment_quantity=fullfilment_quantity, fullfilmen_service=fullfilment_service, fullfilment_status=fullfilment_status, gift_card=gift_card, properties=properties, tip_payment_gateway=tip_payment_gateway, tip_payment_method=tip_payment_method, total_discount_amount=total_discount_amount)
        obj.save()


    def loadorderLocation(self,lineitem_id,country_code = '',province_code = '',name = '',address1 = '',address2 = '',city = '',zip_code = ''):
        OrderLineItem_obj = OrderLineItem.objects.filter(id=lineitem_id)
        obj = OrderLocation(address1=address1, address2=address2, city=city, province_code=province_code, country_code=country_code, name=name, lineitem_id=OrderLineItem_obj, zip_code=zip_code)
        obj.save()
    

    def loadorderNote(self,order_id,note_name = '',note_value = ''):
        order_obj = Order.objects.filter(id=order_id)
        obj = orderNote(order_id=order_obj, note_name=note_name, note_value=note_value)
        obj.save()

    def loadorderTag(self,order_id,tag_name = ''):
        order_obj = Order.objects.filter(id=order_id)
        obj = orderTag(order_id=order_obj, tag_name=tag_name)
        obj.save()

    def loadProductVariant(self,id,image_id,barcode =  '',compare_at_price = 0.0,fullfillment_service=  '',grams =  0.0,inventory_item_id='',position ='',sku = '' ,taxable = False,title = '',updated_at = timezone.now,weight = 0.0,weight_unit = 0.0):
        productImage_obj = ProductImage.objects.filter(id=image_id)
        obj = ProductVariant(updated_at=updated_at, id=id, title=title, position=position, barcode=barcode, compare_at_price=compare_at_price, fullfillment_service=fullfillment_service, grams=grams, image_id=productImage_obj, inventory_item_id=inventory_item_id, sku=sku, taxable=taxable, weight=weight, weight_unit=weight_unit)
        obj.save()
        

    def loadPrerequisiteVariants(self,pricerule_id,varaint_id):
        pricerule_obj = PriceRule.objects.filter(id=pricerule_id)
        productvariant_obj = ProductVariant.objects.filter(id=varaint_id)
        obj = PrerequisiteVariants(pricerule_obj,productvariant_obj)
        obj.save()

    def loadPriceProductVariant(self,price_rule_id,product_variant_id):
        pricerule_obj = PriceRule.objects.filter(id=pricerule_id)
        productvariant_obj = ProductVariant.objects.filter(id=varaint_id)
        obj = PriceProductVariant(pricerule_obj,productvariant_obj)
        obj.save()

    def loadAbandonCartLineItem(self,abandon_cart_id,variant_id,fullfillment_service = '',fullfillment_status = '',required_shipping = False,sku = '',title = '',variant_title = '',vendor = ''):
        abandon_card_obj = AbandonCart.objects.filter(id=abandon_cart_id)
        product_variant_obj = ProductVariant.objects.filter(id=variant_id)
        obj = AbandonCartLineItem(title=title, fullfillment_status=fullfillment_status, vendor=vendor, fullfillment_service=fullfillment_service, sku=sku, abandon_cart_id=abandon_card_obj, required_shipping=required_shipping, variant_id=product_variant_obj, variant_title=variant_title)
        obj.save()
        
