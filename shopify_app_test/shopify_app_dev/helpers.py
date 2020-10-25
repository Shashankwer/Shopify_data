from typing import List
import re
import hmac
import hashlib
import urllib
import datetime
import shopify
from .models import StoreToken
from .Shopify_client import ShopifyStoreClient
from .config import SHOPIFY_API_KEY,SERVER_HOST_NAME,SHOPIFY_API_SECRET_KEY

#SERVER_BASE_URL = f"https://{SERVER_HOST_NAME}"
#INSTALL_REDIRECT_URL = f"{SERVER_BASE_URL}/app_installed"
#WEBHOOK_APP_UNINSTALL_URL = f"https://{SERVER_HOST_NAME}/app_uninstall"
API_VERSION = '2020-10'
STORE_CLIENT = None
def isAppInstalled():
    global STORE_CLIENT
    if len(StoreToken.objects.all())>0:
        obj = StoreToken.objects.get()
        STORE_CLIENT=ShopifyStoreClient(SHOPIFY_API_KEY,SHOPIFY_API_SECRET_KEY,obj.store_url,API_VERSION,obj.token)
        return True
    return False
def generate_install_redirect_url(shop_url:str,scopes:List,nonce:str,access_mode:List):
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
        #print("Success!!")
        return STORE_CLIENT.getStore()
    return "Error"

"""
Shopify's Cursor based ralatvie pagination request and its limitation
MarketingEvents-->Done
Customer-->Address --> Done 
Collect-->Collection-->CollectionImage-->Done
Collect-->Product-->ProductImage-->ProductVariant--Done
PriceRule--> Done
PriceRuleSavedSearch --->Done
PrerequisiteCustomer--> Done
PriceRuleEntity-->PrerequisiteProducts-->PriceRuleProduct-->PrerequisiteVariants-->PriceProductVariant-->Done
DiscountCode
AbandonCart-->AbandonCartLineItem
Order  -->OrderLocation-->orderNote-->orderTag-->OrderLineItem
ClientOrder
OrderdiscountCode

2. DiscountCode
3. AbandonCart
4. Order
. Collect
"""

def getValidDate(d):
    try:
        d = d.split('T')[0]
        date =  datetime.date.today()+datetime.timedelta(100000) if d=='' or d is None else datetime.datetime.strptime(d,"%Y-%m-%d").date()
    except:
        date =  datetime.date.today()+datetime.timedelta(100000)
    return date

def getValidStrField(s):
    try:
        s = s if s is not None else ''
    except:
        s ='' 
    return s

def getValidIntegerField(i):
    try:
        i = int(i) if i is not None else 0
    except: 
        i=0
    return i

def getValidFloatField(f):
    try:
        f = float(f) if f is not None else 0.0
    except:
        f=0.0
    return f

def getValidBooleanField(b):
    b = True if b else False
    return b

def load_marketingevent(market):    
    STORE_CLIENT.loadMarketingEvents(
        id=getValidStrField(market.id), 
        remote_id=getValidStrField(market.remote_id),
        event_type=getValidStrField(market.event_type), 
        marketing_channel=getValidStrField(market.marketing_channel), 
        paid=getValidBooleanField(market.paid),
        referring_domain=getValidStrField(market.referring_domain),
        budget=getValidFloatField(market.budget),
        currency=getValidStrField(market.currency), 
        budget_type=getValidStrField(market.budget_type),
        started_at=getValidDate(market.started_at),
        scheduled_end_at = getValidDate(market.schedule_to_end_at),
        ended_at=getValidDate(market.ended_at),
        utm_campaign=getValidStrField(market.utm_campaign),
        utm_source=getValidStrField(market.utm_source),
        utm_medium=getValidStrField(market.utm_medium), 
        description=getValidStrField(market.description),
        manage_url=getValidStrField(market.manage_url),
        preview_url=getValidStrField(market.preview_url),
        marketing_resource=",".join(market.marketed_resources)
    )
    return True

def get_marketingEvents_details():
    if isAppInstalled():
        count = 0 
        marketingEvent, rel = STORE_CLIENT.getMarketingEvents()
        count+= len(marketingEvent)
        for market in marketingEvent:
            if not STORE_CLIENT.isMarketPresent(market.id):
                load_marketingevent(market) 
        while rel!='':
            marketingEvent,rel = STORE_CLIENT.getMarketingEvents(link=rel)
            for market in marketingEvent:
                if not STORE_CLIENT.isMarketPresent(market.id):
                    load_marketingevent(market)
            count+= len(marketingEvent)
        print(len(marketingEvent))
        return count
    return "Error"

def load_customer_details(customer):
    customer_id = customer.id
    STORE_CLIENT.loadCustomer(
        identity = getValidStrField(customer_id),
        last_order_id=getValidStrField(customer.last_order_id),
        email = getValidStrField(customer.email),
        accept_marketing=getValidStrField(customer.accepts_marketing),
        created_at= getValidDate(customer.created_at),
        updated_at = getValidDate(customer.updated_at),
        first_name=getValidStrField(customer.first_name),
        last_name=getValidStrField(customer.last_name),
        order_count=getValidIntegerField(customer.orders_count),
        state=getValidStrField(customer.state),
        total_spent=getValidFloatField(customer.total_spent),
        multi_pass_identifier=getValidStrField(customer.multipass_identifier),
        tax_exempt = getValidBooleanField(customer.tax_exempt),
        tags = getValidStrField(customer.tags),
        last_order_name=getValidStrField(customer.last_order_name),
        currency = getValidStrField(customer.currency),
        marketing_optin_level=getValidStrField(customer.marketing_opt_in_level)
    )
    print(customer_id)
    for address in customer.addresses:
        address_id = getValidStrField(address.id)
        if not STORE_CLIENT.isAddressPresent(address_id):
            STORE_CLIENT.loadAddress(
            address_id = address_id,
            address_type = "Customer address",
            company = getValidStrField(address.company),
            address1=getValidStrField(address.address1),
            address2=getValidStrField(address.address2), 
            city=getValidStrField(address.city), 
            country=getValidStrField(address.country), 
            zipcode=getValidStrField(address.zip), 
            default=getValidBooleanField(address.default), 
            province_code=getValidStrField(address.province_code), 
            country_code=getValidStrField(address.country_code),
            first_name=getValidStrField(address.first_name), 
            last_name=getValidStrField(address.last_name)
            )
            default = getValidBooleanField(address.default)
            STORE_CLIENT.loadCustomerAddress(customer_id,address_id,default)
        if not STORE_CLIENT.isAddressPresent(customer.default_address.id):
            print("Default Not found")
            address_id = getValidStrField(customer.default_address.id)
            STORE_CLIENT.loadAddress(
                address_id = address_id,
                address_type = "Customer address",
                company = getValidStrField(customer.default_address.company),
                address1=getValidStrField(customer.default_address.address1),
                address2=getValidStrField(customer.default_address.address2), 
                city=getValidStrField(customer.default_address.city), 
                country=getValidStrField(customer.default_address.country), 
                zipcode=getValidStrField(customer.default_address.zip), 
                default=getValidBooleanField(customer.default_address.default), 
                province_code=getValidStrField(customer.default_address.province_code), 
                country_code=getValidStrField(customer.default_address.country_code),
                first_name=getValidStrField(customer.default_address.first_name), 
                last_name=getValidStrField(customer.default_address.last_name)
            )
            default = True
            STORE_CLIENT.loadCustomerAddress(customer_id,address_id,default)
    return True

def get_customer_details():
    if isAppInstalled():
        count=0
        customers,rel=STORE_CLIENT.getCustomer()
        for customer in customers:
            if not STORE_CLIENT.isCustomerPresent(customer.id):
                load_customer_details(customer)
        count+=len(customers)
        while rel!='':
            customers,rel=STORE_CLIENT.getCustomer(link=rel)     
            for customer in customers:
                if not STORE_CLIENT.isCustomerPresent(customer.id):
                    load_customer_details(customer)
            count+=len(customers)  
        return count
    return "Error"

def load_product(product):
    product_id = product.id
    STORE_CLIENT.loadProduct(
        id=getValidStrField(product.id), 
        body_html=getValidStrField(product.body_html),
        handle=getValidStrField(product.handle), 
        product_type=getValidStrField(product.product_type),
        published_scope=getValidStrField(product.published_scope),
        status=getValidStrField(product.status),
        published_date=getValidDate(product.published_at),
        update_at=getValidDate(product.updated_at),
        tags=getValidStrField(product.tags),
        template_suffix=getValidStrField(product.template_suffix),
        title=getValidStrField(product.title),
        vendor=getValidStrField(product.vendor)
    )
    
    for product_image in product.images:
        if not STORE_CLIENT.isProductImagePresent(product_image.id):
            STORE_CLIENT.loadProductImage(
                product_id=product_id, 
                id=getValidStrField(product_image.id),
                position=getValidStrField(product_image.position),
                src=getValidStrField(product_image.src),
                width=getValidIntegerField(product_image.height), 
                height=getValidIntegerField(product_image.width),
                update_at=getValidDate(product_image.updated_at)
            )
    for variant in product.variants:
        if not STORE_CLIENT.isProductVariantPresent(variant.id):
            STORE_CLIENT.loadProductVariant(
                id=variant.id, 
                image_id=getValidStrField(variant.image_id),
                barcode=getValidStrField(variant.barcode),
                compare_at_price=getValidFloatField(variant.compare_at_price),
                fullfillment_service=getValidStrField(variant.fulfillment_service),
                grams=getValidFloatField(variant.grams),
                inventory_item_id=getValidStrField(variant.inventory_item_id),
                position=getValidIntegerField(variant.position), 
                sku=getValidStrField(variant.sku), 
                taxable=getValidBooleanField(variant.taxable),
                title=getValidStrField(variant.title),
                updated_at=getValidDate(variant.updated_at),
                weight=getValidFloatField(variant.weight),
                weight_unit=getValidStrField(variant.weight_unit),
                product_id=product_id
            )
    for option in product.options:
        if not STORE_CLIENT.isProductOptionPresent(option.id):
            STORE_CLIENT.loadProductOption(
                id=getValidStrField(option.id), 
                name=getValidStrField(option.name),
                product=product_id,
                position=getValidIntegerField(option.position),
                values=getValidStrField(option.values)
            )


    #for variant in product.variants:
    #   if not STORE_CLIENT.isProductVariantPresent(variant.id):
            
def get_product_details():
    if isAppInstalled():
        count=0
        products,rel =  STORE_CLIENT.getProduct(link="")
        for product in products:
            load_product(product)
        count+=len(products)
        while rel !='':
            products,rel =  STORE_CLIENT.getProduct(link=rel)
            for product in products:
                load_product(product)
            count+=len(products)
        return count
    return "Error"

def loadCollection(col):
    STORE_CLIENT.loadCollection(
        id=getValidStrField(col.id), 
        body_html=getValidStrField(col.body_html),
        handle=getValidStrField(col.handle), 
        published_at=getValidDate(col.published_at),
        published_scope=getValidStrField(col.published_scope),
        sort_order=getValidStrField(col.sort_order),
        title=getValidStrField(col.title),
        update_at=getValidDate(col.updated_at)
    )

def get_customcollection_details():
    if isAppInstalled():
        count = 0
        collections,rel = STORE_CLIENT.getCustomCollection(link ='')
        for collection in collections:
            if not STORE_CLIENT.isCollectionPresent(collection.id):
                loadCollection(collection)
        count+=len(collections)
        while rel !='':
            collections,rel = STORE_CLIENT.getCustomCollection(link=rel)
            for collection in collections:
                if not STORE_CLIENT.isCollectionPresent(collection.id):
                   loadCollection(collection)
            count+=len(collections)
        return count
    return "Error"

def get_smartcollection_details():
    if isAppInstalled():
        count = 0
        collections,rel = STORE_CLIENT.getSmartCollection(link ='')
        for collection in collections:
            if not STORE_CLIENT.isCollectionPresent(collection.id):
                loadCollection(collection)
        count+=len(collections)
        while rel !='':
            collections,rel = STORE_CLIENT.getCustomCollection(link=rel)
            for collection in collections:
                if not STORE_CLIENT.isCollectionPresent(collection.id):
                   loadCollection(collection)
            count+=len(collections)
        return count
    return "Error"

def load_collect_details(collect):
    STORE_CLIENT.loadCollect(
        id = getValidStrField(collect.id),
        collection_id=getValidStrField(collect.collection_id), 
        product_id=getValidStrField(collect.product_id), 
        created_at=getValidDate(collect.created_at),
        position=getValidIntegerField(collect.position),
        updated_at=getValidDate(collect.updated_at)
    )

def get_collect_details():
    if isAppInstalled():
        count = 0
        collects,rel = STORE_CLIENT.getCollect(link='')
        for collect in collects:
            if not STORE_CLIENT.isCollectPresent(collect.id):
                load_collect_details(collect)
        count+=len(collects)
        while rel !='':
            collects,rel = STORE_CLIENT.getCustomCollection(link=rel)
            for collect in collects:
                if not STORE_CLIENT.isCollectPresent(collect.id):
                   load_collect_details(collect)
            count+=len(collects)
        return count
    return "Error"

def load_price_rule_details(price_rule):
    price_rule_id = price_rule.id
    print(price_rule_id)
    STORE_CLIENT.loadPriceRule(
        id=getValidStrField(price_rule.id), 
        allocation_method=getValidStrField(price_rule.allocation_method),
        created_at=getValidDate(price_rule.created_at),
        updated_at=getValidDate(price_rule.updated_at),
        customer_selection=getValidStrField(price_rule.customer_selection), 
        ends_at=getValidDate(price_rule.ends_at),
        once_per_customer=getValidBooleanField(price_rule.once_per_customer),
        prerequisite_quantity_range=getValidIntegerField(price_rule.prerequisite_quantity_range),
        prerequisite_shipping_price_range=getValidFloatField(price_rule.prerequisite_shipping_price_range),
        prerequisite_subtotal_range=getValidFloatField(price_rule.prerequisite_subtotal_range),
        prerequisite_purchase=getValidFloatField(price_rule.prerequisite_subtotal_range),
        starts_at=getValidDate(price_rule.starts_at),
        target_selection=getValidStrField(price_rule.target_selection),
        target_type=getValidStrField(price_rule.target_type),
        title=getValidStrField(price_rule.title),
        usage_limit=getValidIntegerField(price_rule.usage_limit)
    )
    for saved in price_rule.prerequisite_saved_search_ids:
        STORE_CLIENT.loadPriceRuleSavedSearch(price_rule_id,saved)

    for product in price_rule.prerequisite_product_ids:
        STORE_CLIENT.loadPrerequisiteProducts(price_rule_id,product)
    
    for customer in price_rule.prerequisite_customer_ids:
        STORE_CLIENT.loadPrerequisiteCustomer(price_rule_id,customer)

    for variant in price_rule.prerequisite_variant_ids:
        STORE_CLIENT.loadPrerequisiteVariants(price_rule_id,variant)

    for variant in price_rule.entitled_variant_ids:
        STORE_CLIENT.loadPriceProductVariant(price_rule_id,variant)    
    
    for collection in price_rule.entitled_collection_ids:
        STORE_CLIENT.loadPriceRuleEntity(price_rule_id,collection)
    
    for product in price_rule.entitled_product_ids:
        STORE_CLIENT.loadPriceRuleProduct(price_rule_id,product)

    for variant in price_rule.entitled_variant_ids:
        STORE_CLIENT.loadPriceProductVariant(price_rule_id,variant)
    discount_codes = STORE_CLIENT.getDiscountCode(price_rule_id)
    for discount_code in discount_codes:
        load_discount_code(discount_code)
    print("Inserted into DB")
        

def get_price_rule_details():
    if isAppInstalled():
        count = 0
        price_rules,rel = STORE_CLIENT.getPriceRule(link='')
        for price_rule in price_rules:
            if not STORE_CLIENT.isPriceRulePresent(price_rule.id):
                load_price_rule_details(price_rule)
        count+=len(price_rules)
        while rel !='':
            price_rules,rel = STORE_CLIENT.getCustomCollection(link=rel)
            for price_rule in price_rules:
                if not STORE_CLIENT.isPriceRulePresent(price_rule.id):
                   load_price_rule_details(price_rule)
            count+=len(price_rules)
        return count
    return "Error"

def load_discount_code(discount_code):
    STORE_CLIENT.loadDiscountCode(
        id=getValidStrField(discount_code.id), 
        price_rule_id=getValidStrField(discount_code.price_rule_id), 
        code=getValidStrField(discount_code.code), 
        useage_count=getValidStrField(discount_code.usage_count),
        created_at=getValidDate(discount_code.created_at),
        updated_at=getValidDate(discount_code.updated_at)
    )
    
def get_order_details():
    if isAppInstalled():
        print("Success!!")
        return "Testing"
    return "Error"
       

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

