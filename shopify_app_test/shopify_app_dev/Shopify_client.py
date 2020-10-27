import json
from typing import List
import logging
import requests
from requests.exceptions import HTTPError
import shopify
from .models import StoreToken
from django.utils import timezone
from .models import PriceRule,PriceRuleSavedSearch,DiscountCode
from .models import MarketingEvents,Address,Customer,CustomerAddress
from .models import PrerequisiteCustomer,AbandonCart,Order,ClientOrder
from .models import OrderdiscountCode,Collection,PriceRuleEntity,Product
from .models import PrerequisiteProducts,PriceRuleProduct,ProductImage
from .models import Collect,CollectionImage,OrderLineItem,AbandonCartLineItem
from .models import PriceProductVariant,orderNote,orderTag,ProductVariant
from .models import PrerequisiteVariants,OrderLocation,ProductOptions


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
    
    #The function gets the link
    def getRelLink(self,link=''):
        links=link.split(",")
        rel = ""
        for l in links:
            if l[l.find("rel"):].find("next")!=-1:
                print(link)
                rel=l.split(';')[0].replace(">",'').split("=")[-1]
        return rel        
    
    def getMarketingEvents(self,link='',limit=250):
        """
        link defines the next page reference if there exists any
        limit: int describing the number of records to be loaded at a single time
        """
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        marketingEvents = shopify.MarketingEvent.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return marketingEvents,rel
    
    def getCustomer(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        customers = shopify.Customer.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return customers,rel

    def getStore(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current()
        shopify.ShopifyResource.clear_session()
        return shop

    def getProduct(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        products = shopify.Product.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return products,rel

    def getProductVariants(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        productVariant = shopify.Variant.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return productVariant

    def getCustomCollection(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        collection = shopify.CustomCollection.find(limit=limit,page_info=link)
        #SmartCollection.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        return collection,rel

    def getSmartCollection(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        collection = shopify.SmartCollection.find(limit=limit,page_info=link)
        #SmartCollection.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        return collection,rel        

    def getCollect(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session)
        collect = shopify.Collect.find(limit=limit,page_info=link)
        rel = ''
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        shopify.ShopifyResource.clear_session()
        return collect,rel
    
    def getPriceRule(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        price_rules = shopify.PriceRule.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return price_rules,rel

    def getDiscountCode(self,price_rule_id):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        discount_codes = shopify.DiscountCode.find(price_rule_id=price_rule_id)
        shopify.ShopifyResource.clear_session()
        return discount_codes

    def getAbandondedCart(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        abandon = shopify.Checkout.find(limit=limit,page_info=link)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return abandon,rel

    def getOrder(self,link='',limit=250):
        shopify.Session.setup(api_key=self.api_key, secret=self.secret_key)
        session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(session) 
        orders = shopify.Order.find(limit=limit,page_info=link)
        print(orders)
        if 'Link' in shopify.ShopifyResource.connection.response.headers:
            headers = shopify.ShopifyResource.connection.response.headers['Link']
            if headers is not None:
                rel = self.getRelLink(headers)
        else:
            rel = ''
        shopify.ShopifyResource.clear_session()
        return orders,rel

    def loadPriceRule(self,id,allocation_method = '',created_at=timezone.now,updated_at = timezone.now,customer_selection = '',ends_at = timezone.now,once_per_customer = True,prerequisite_quantity_range = 1,prerequisite_shipping_price_range = '',prerequisite_subtotal_range = 0.0,prerequisite_purchase = 0.0,starts_at = timezone.now,target_selection = '',target_type = '',title= '',usage_limit = 10):
        obj = PriceRule(allocation_method=allocation_method, created_at=created_at, updated_at=updated_at, customer_selection=customer_selection, ends_at=ends_at, id=id, once_per_customer=once_per_customer, prerequisite_quantity_range=prerequisite_quantity_range, prerequisite_shipping_price_range=prerequisite_shipping_price_range, prerequisite_subtotal_range=prerequisite_subtotal_range, prerequisite_purchase=prerequisite_purchase, starts_at=starts_at, target_selection=target_selection, target_type=target_type, title=title, usage_limit=usage_limit)
        obj.save()

    def loadPriceRuleSavedSearch(self,price_rule_id,saved_search=''):
        obj = PriceRuleSavedSearch(price_rule=PriceRule.objects.get(id=price_rule_id), saved_search=saved_search)
        obj.save()

    def loadDiscountCode(self,id, price_rule_id,code='',useage_count='',created_at= timezone.now,updated_at = timezone.now):
        obj = DiscountCode(created_at=created_at, updated_at=updated_at, id=id, price_rule=PriceRule.objects.get(id=price_rule_id), code=code, useage_count=useage_count)
        obj.save()

    def loadMarketingEvents(self,id,remote_id='',event_type = '',marketing_channel = '',paid = '',referring_domain = '',budget = 0,currency = '',budget_type = '',started_at = timezone.now,scheduled_end_at = timezone.now,ended_at = timezone.now,utm_campaign = '',utm_source = '',utm_medium = '',description = '',manage_url = '',preview_url = '',marketing_resource = ''):
        obj = MarketingEvents(id=id,remote_id = remote_id,event_id =event_type,marketing_channel= marketing_channel,paid= paid,referring_domain = referring_domain,budget= budget,currency= currency,budget_type= budget_type,started_at= started_at,scehduled_end_at = scheduled_end_at,ended_at = ended_at,utm_campaign= utm_campaign,utm_source= utm_source,utm_medium= utm_medium,decription= description,manage_url= manage_url,preview_url= preview_url,marketing_resource= marketing_resource) 
        obj.save()       

    def loadAddress(self,address_id,
                    address_type = '',
                    company =  '',
                    address1 =  '',
                    address2 =  '',
                    city =  '',
                    latitude = '',
                    longitutde  = '',
                    country =  '',
                    zipcode =  '',
                    default = False,
                    province_code = '',
                    country_code = '',
                    first_name = '',
                    last_name = '',
                    billing_Address_type = ''):
        obj = Address(default=default, address_type=address_type, address_id=address_id, company=company, address1=address1, address2=address2, city=city, latitude=latitude, longitutde=longitutde, country=country, zipcode=zipcode, province_code=province_code, country_code=country_code, first_name=first_name, last_name=last_name, billing_Address_type=billing_Address_type)
        obj.save()

    def loadCustomer(self,identity,last_order_id ='',email = '',accept_marketing = False,created_at = timezone.now,updated_at = timezone.now,first_name = '',last_name = '',order_count = 0,state = '',total_spent = 0,multi_pass_identifier = '',tax_exempt=False,tags = '',last_order_name = '',currency = '',marketing_optin_level = ''):
        obj = Customer(created_at=created_at, updated_at=updated_at, id=identity, currency=currency, first_name=first_name, last_name=last_name, email=email, accept_marketing=accept_marketing, order_count=order_count, state=state, total_spent=total_spent, last_order_id=last_order_id, multi_pass_identifier=multi_pass_identifier, tax_exempt=tax_exempt, tags=tags, last_order_name=last_order_name, marketing_optin_level=marketing_optin_level)
        obj.save()

    def loadCustomerAddress(self,customer_id,address_id,default = False):
        obj = CustomerAddress(customer=Customer.objects.get(id=customer_id),address=Address.objects.get(address_id = address_id),default=default)
        obj.save()

    def loadPrerequisiteCustomer(self,price_rule_id,customer_id):
        obj = PrerequisiteCustomer(price_rule=PriceRule.objects.get(id=price_rule_id),customer=Customer.objects.get(id=customer_id))
        obj.save()
    
    def loadAbandonCart(self,id,customer_id,user_id='',device_id='',buyer_accepts_marketing=False,cart_token = '',completed_at = timezone.now,created_at = timezone.now,customer_locale = '',gateway  = '',landing_site='',location = '',note = '',currency_code = '',referring_site = '',source_name = '',subtotal_price = 0.0,tokens = '',total_discount = 0.0,total_price = 0.0,total_weight = 0.0,updated_at = timezone.now):
        obj = AbandonCart(created_at=created_at, updated_at=updated_at, id=id, note=note, customer=Customer.objects.get(id=customer_id), buyer_accepts_marketing=buyer_accepts_marketing, cart_token=cart_token, completed_at=completed_at, customer_locale=customer_locale, device_id=device_id, gateway=gateway, landing_site=landing_site, location=location, currency_code=currency_code, referring_site=referring_site, source_name=source_name, subtotal_price=subtotal_price, tokens=tokens, total_discount=total_discount, total_price=total_price, total_weight=total_weight, user_id=user_id)
        obj.save()

    def loadOrder(self,id,customer_id,app_id='',browser_ip = '',buyer_accepts_marketing = False,cancel_reason = '',cancelled_at = timezone.now,cart_token = '',checkout_id='',closed_at = timezone.now,created_at = timezone.now,currency = '',customer_locale = '',order_email = '',order_financial_status = '',fullfillment_status = '',gateway = '',landing_site = '',landing_site_ref = ''    ,name = '',notes = '',number = 0,order_number= 0,payment_gateway = '',presenment_currency = '',referring_site = '',source_name = '',total_discount = 0.0,total_line_item_price = 0.0,total_price = 0.0,total_line_tax = 0.0,total_tip = 0.0,user_id='',update_at = timezone.now,total_weight = ''):
        obj = Order(created_at=created_at, id=id, currency=currency, customer=Customer.objects.get(id=customer_id), buyer_accepts_marketing=buyer_accepts_marketing, cart_token=cart_token, customer_locale=customer_locale, gateway=gateway, landing_site=landing_site_ref, referring_site=referring_site, source_name=source_name, total_discount=total_discount, total_price=total_price, total_weight=total_weight, user_id=user_id, app_id=app_id, browser_ip=browser_ip, cancel_reason=cancel_reason, cancelled_at=cancelled_at, checkout_id=checkout_id, closed_at=closed_at, order_email=order_email, order_financial_status=order_financial_status, fullfillment_status=fullfillment_status, landing_site_ref=landing_site_ref, name=name, notes=notes, number=number, order_number=order_number, payment_gateway=payment_gateway, presenment_currency=presenment_currency, total_line_item_price=total_line_item_price, total_line_tax=total_line_tax, total_tip=total_tip, update_at=update_at)
        obj.save()
    
    def loadClientOrder(self,order_id,accept_language = '',browser_height = '',browser_width = '',session_hash = '',user_hash = ''):
        obj = ClientOrder(order=Order.objects.get(id=order_id), accept_language=accept_language, browser_height=browser_height, browser_width=browser_width, session_hash=session_hash, user_hash=user_hash)
        obj.save()

    def loadOrderdiscountCode(self,discount_code,order_id=None,abandoncart_id=None):
        if order_id is not None:
            obj = OrderdiscountCode(order=Order.objects.get(id=order_id), abandoncart=abandoncart_id, discount_codes=DiscountCode.objects.get(code=discount_code))
            obj.save()
        elif abandoncart_id is not None:
            obj = OrderdiscountCode(order=order_id, abandoncart=AbandonCart.objects.get(id=abandoncart_id), discount_codes=DiscountCode.objects.get(id=discount_code))
            obj.save()

    def loadCollection(self,id ,body_html='',handle = '',published_at = timezone.now,published_scope = '',sort_order = '',title = '',update_at = timezone.now):
        obj = Collection(id=id, title=title, update_at=update_at, body_html=body_html, handle=handle, published_at=published_at, published_scope=published_scope, sort_order=sort_order)
        obj.save()
    
    def loadPriceRuleEntity(self,price_rule_id,collection_id):
        obj =PriceRuleEntity(price_rule=PriceRule.objects.get(id=price_rule_id), collection=Collection.objects.get(id=collection_id))
        obj.save()

    def loadProduct(self,
                    id,
                    body_html='',
                    handle = '',
                    product_type = '',
                    published_scope = '',
                    status = '',
                    published_date = timezone.now,
                    update_at = timezone.now,
                    tags = '',
                    template_suffix = '',
                    title = '',
                    vendor = ''):
        obj = Product(id=id, title=title, tags=tags, update_at=update_at, body_html=body_html, handle=handle, published_scope=published_scope, product_type=product_type, status=status, published_date=published_date, template_suffix=template_suffix, vendor=vendor)
        obj.save()
    
    def loadProductOption(self,id, name='', product='', position=0, values=''):
        obj = ProductOptions(id=id, name=name, product=Product.objects.get(id=product), position=position, values=values)
        obj.save()

    def loadPrerequisiteProducts(self,pricerule_id,product_id):
        obj = PrerequisiteProducts(pricerule=PriceRule.objects.get(id=pricerule_id),product=Product.objects.get(id=product_id))
        obj.save()

    def loadPriceRuleProduct(self,price_rule_id,product_id):
        obj = PriceRuleProduct(price_rule=PriceRule.objects.get(id=price_rule_id),product=Product.objects.get(id=product_id))
        obj.save()    

    def loadProductImage(self,product_id,id,position = -1,src = '',width = 0,height = 0,update_at = timezone.now):
        obj = ProductImage(id=id, update_at=update_at, product=Product.objects.get(id = product_id), position=position, src=src, width=width, height=height)
        obj.save()

    def loadCollect(self,id,collection_id,product_id,created_at = timezone.now,position = -1,updated_at = timezone.now):
        obj = Collect(created_at=created_at, updated_at=updated_at, id=id, collection=Collection.objects.get(id=collection_id), product=Product.objects.get(id=product_id), position=position)
        obj.save()
    
    def loadCollectionImage(self,collection_id,src = '',alt = '',created_at = timezone.now,width = 0,height = 0):
        collection_obj = Collection.objects.get(id = collection_id)
        obj = CollectionImage(created_at, collection_obj, src, width, height, alt)
        obj.save()

    def loadOrderLineItem(self,id,order_id,product_id,variant_id,fullfilment_quantity='',fullfilment_service = '',fullfilment_status = '',vendor = '',name = '',gift_card = '',taxable = False,tip_payment_gateway = '',tip_payment_method = '',total_discount_amount = 0.0,properties=''):
        obj = OrderLineItem(id=id, name=name, order=Order.objects.get(id=order_id), vendor=vendor, product=Product.objects.get(id=product_id), taxable=taxable, variant=ProductVariant.objects.get(id=variant_id), fullfilment_quantity=fullfilment_quantity, fullfilmen_service=fullfilment_service, fullfilment_status=fullfilment_status, gift_card=gift_card, properties=properties, tip_payment_gateway=tip_payment_gateway, tip_payment_method=tip_payment_method, total_discount_amount=total_discount_amount) 
        obj.save()


    def loadorderLocation(self,lineitem_id,country_code = '',province_code = '',name = '',address1 = '',address2 = '',city = '',zip_code = ''):
        OrderLineItem_obj = OrderLineItem.objects.get(id=lineitem_id)
        obj = OrderLocation(address1=address1, address2=address2, city=city, province_code=province_code, country_code=country_code, name=name, lineitem_id=OrderLineItem_obj, zip_code=zip_code)
        obj.save()
    

    def loadorderNote(self,order_id,note_name = '',note_value = ''):
        obj = orderNote(order=Order.objects.get(id=order_id), note_name=note_name, note_value=note_value)
        obj.save()

    def loadorderTag(self,order_id,tag_name = ''):
        obj = orderTag(order=Order.objects.get(id=order_id), tag_name=tag_name)
        obj.save()

    def loadProductVariant(self,id,product_id,image_id='',barcode =  '',compare_at_price = 0.0,fullfillment_service=  '',grams =  0.0,inventory_item_id='',position ='',sku = '' ,taxable = False,title = '',updated_at = timezone.now,weight = 0.0,weight_unit = ''):
        obj = ProductVariant(updated_at=updated_at, id=id, title=title, position=position, barcode=barcode,
                 compare_at_price=compare_at_price, 
                 fullfillment_service=fullfillment_service,
                 grams=grams, 
                 image_id=image_id,
                 inventory_item_id=inventory_item_id,
                 sku=sku, 
                 taxable=taxable,
                 weight=weight,
                 weight_unit=weight_unit,
                 product=Product.objects.get(id=product_id))
        obj.save()
        

    def loadPrerequisiteVariants(self,pricerule_id,variant_id):
        obj = PrerequisiteVariants(pricerule=PriceRule.objects.get(id=pricerule_id),varaint=ProductVariant.objects.get(id=variant_id))
        obj.save()

    def loadPriceProductVariant(self,price_rule_id,product_variant_id):
        obj = PriceProductVariant(price_rule=PriceRule.objects.get(id=price_rule_id),product_variant=ProductVariant.objects.get(id=product_variant_id))
        obj.save()

    def loadAbandonCartLineItem(self,abandon_cart_id,variant_id,fullfillment_service = '',fullfillment_status = '',required_shipping = False,sku = '',title = '',variant_title = '',vendor = ''):
        obj = AbandonCartLineItem(title=title, fullfillment_status=fullfillment_status, vendor=vendor, fullfillment_service=fullfillment_service, sku=sku, abandon_cart=AbandonCart.objects.get(id=abandon_cart_id), required_shipping=required_shipping, variant=ProductVariant.objects.get(id=variant_id))
        obj.save()

    def isMarketPresent(self,market_id):
        try: 
            MarketingEvents.objects.get(id=market_id)
            return True
        except:
            return False

    def isCustomerPresent(self,customer_id):
        try: 
            Customer.objects.get(id=customer_id)
            return True
        except:
            return False

    def isAddressPresent(self,address_id):
        try: 
            Address.objects.get(address_id=address_id)
            return True
        except:
            return False

    def isProductPresent(self,product_id):
        try:
            Product.objects.get(id=product_id)
            return True
        except:
            return False

    def isProductVariantPresent(self,product_variant_id):
        try:
            ProductVariant.objects.get(id=product_variant_id)
            return True
        except:
            return False        

    def isProductOptionPresent(self,product_option_id):
        try:
            ProductOptions.objects.get(id=product_option_id)
            return True
        except:
            return False                

    def isProductImagePresent(self,product_image_id):
        try:
            ProductImage.objects.get(id=product_image_id)
            return True
        except:
            return False        

    def isCollectionPresent(self,collection_id):
        try:
            Collection.objects.get(id=collection_id)
            return True
        except:
            return False
    
    def isCollectPresent(self,collect_id):
        try:
            Collect.objects.get(id=collect_id)
            return True
        except:
            return False

    def isPriceRulePresent(self,pricerule_id):
        try:
            PriceRule.objects.get(id=pricerule_id)
            return True
        except:
            return False

    def isDiscountCodePresent(self,discount_id):
        try:
            DiscountCode.objects.get(id=discount_id)
            return True
        except:
            return False

    def isAbandonPresent(self,abandon_id):
        try:
            AbandonCart.objects.get(id=abandon_id)
            return True
        except:
            return False                

    def isOrderPresent(self,order_id):
        try:
            Orders.objects.get(id=order_id)
            return True
        except:
            return False                