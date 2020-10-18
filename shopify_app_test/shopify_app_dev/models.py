from django.db import models
from django.db import models
from django.utils import timezone
from datetime import date

class StoreToken(models.Model):
    token = models.CharField(max_length=1000)
    store_url = models.CharField(max_length=1000,default='')

class PriceRule(models.Model):
    allocation_method = models.CharField(max_length=20)
    created_at=models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)    
    customer_selection = models.CharField(max_length=200)
    ends_at = models.DateField(default=timezone.now)
    id = models.CharField(max_length=200,primary_key=True)
    once_per_customer = models.BooleanField(default=True)
    prerequisite_quantity_range = models.IntegerField(default=1)
    prerequisite_shipping_price_range = models.CharField(max_length=200,default='')
    prerequisite_subtotal_range = models.FloatField(default=0.0)
    prerequisite_purchase = models.FloatField(default=0.0)
    starts_at = models.DateField(default=timezone.now)
    target_selection = models.CharField(max_length=200,default='')
    target_type = models.CharField(max_length=200,default='')
    title= models.CharField(max_length=200)
    usage_limit = models.IntegerField(default=10)

class PriceRuleSavedSearch(models.Model):
    price_rule = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    saved_search = models.CharField(max_length=200)


class DiscountCode(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    price_rule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    useage_count = models.IntegerField(default=0)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)

class MarketingEvents(models.Model):
    remote_id = models.CharField(max_length=200,default='')
    event_type = models.CharField(max_length=100,default='')
    marketing_channel = models.CharField(max_length=10,default='')
    paid = models.CharField(max_length=10,default='')
    referrring_domain = models.CharField(max_length=1000,default='')
    budget = models.IntegerField(default =0)
    currency = models.CharField(max_length=10,default='')
    budget_type = models.CharField(max_length=3,default='')
    started_at = models.DateField(default=timezone.now)
    scheduled_end_at = models.DateField(default=timezone.now)
    ended_at = models.DateField(default=timezone.now)
    utm_campaign = models.CharField(max_length=10,default='')
    utm_source = models.CharField(max_length=10,default='')
    utm_medium = models.CharField(max_length=10,default='')
    description = models.CharField(max_length=100,default='')
    manage_url = models.CharField(max_length=100,default='')
    preview_url = models.CharField(max_length=100,default='')
    marketing_source = models.CharField(max_length=100,default='')

class Address(models.Model):
    address_type = models.CharField(max_length=200,default='')
    address_id = models.CharField(max_length=200,default='')
    company =  models.CharField(max_length=200,default='')
    address1 =  models.CharField(max_length=200,default='')
    address2 =  models.CharField(max_length=200,default='')
    city =  models.CharField(max_length=400,default='')
    latitude = models.CharField(max_length=100,default='')
    longitutde  = models.CharField(max_length=100,default='')
    country =  models.CharField(max_length=400,default='')
    zipcode =  models.CharField(max_length=10,default='')
    default = models.BooleanField(default=False)
    province_code = models.CharField(max_length=30,default='')
    country_code = models.CharField(max_length=100,default='')
    first_name = models.CharField(max_length=1000,default='')
    last_name = models.CharField(max_length=1000,default='')
    billing_Address_type = models.CharField(max_length=20,default='')


class Customer(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    email = models.EmailField(default='')
    accept_marketing = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    first_name = models.CharField(max_length=200,default='')
    last_name = models.CharField(max_length=200,default='')
    order_count = models.IntegerField(default=0)
    state = models.CharField(max_length=100,default='')
    total_spent = models.IntegerField(default=0)
    last_order_id = models.CharField(max_length=200,default='')
    multi_pass_identifier = models.CharField(max_length=200,default='')
    tax_exempt=models.BooleanField(default=False)
    tags = models.CharField(max_length=1000)
    last_order_name = models.CharField(max_length=400,default='')
    currency = models.CharField(max_length=100,default='')
    marketing_optin_level = models.CharField(max_length=100,default='')

class CustomerAddress(models.Model):
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address,on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

class PrerequisiteCustomer(models.Model):
    price_rule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete =models.CASCADE)

class AbandonCart(models.Model):
    buyer_accepts_marketing=models.BooleanField(default=False)
    cart_token = models.CharField(max_length=100,default='')
    completed_at = models.DateField(default=timezone.now)
    created_at = models.DateField(default=timezone.now)
    customer_locale = models.CharField(max_length=10,default='')
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    device_id = models.CharField(max_length=200,default='')
    gateway  = models.CharField(max_length=200,default='')
    id = models.CharField(max_length=200,primary_key=True)
    landing_site=models.CharField(max_length=400,default='')
    location = models.CharField(max_length=200,default='')
    note = models.CharField(max_length=100,default='')
    currency_code = models.CharField(max_length=6,default='')
    referring_site = models.CharField(max_length=400,default='')
    source_name = models.CharField(max_length=400,default='')
    subtotal_price = models.FloatField(default=0.0)
    tokens = models.CharField(max_length=200,default='')
    total_discount = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    total_weight = models.FloatField(default=0.0)
    updated_at = models.DateField(default=timezone.now)
    user_id = models.CharField(max_length=200,default='')


class Order(models.Model):
    app_id = models.CharField(max_length=200,default='')
    browser_ip = models.CharField(max_length=200,default='')
    buyer_accepts_marketing = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=200,default='')
    cancelled_at = models.DateField(default=timezone.now)
    cart_token = models.CharField(max_length=200,default='')
    checkout_id = models.CharField(max_length=200,default='')
    closed_at = models.DateField(default=timezone.now)
    created_at = models.DateField(default=timezone.now)
    currency = models.CharField(max_length=6,default='')
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customer_locale = models.CharField(max_length=20,default='')
    order_email = models.CharField(max_length=200,default='')
    order_financial_status = models.CharField(max_length=30,default='')
    fullfillment_status = models.CharField(max_length=200,default='')
    gateway = models.CharField(max_length=20,default='')
    id = models.CharField(max_length=200,primary_key=True)
    landing_site = models.CharField(max_length=200,default='')
    landing_site_ref = models.CharField(max_length=200,default='')    
    name = models.CharField(max_length=200,default='')
    notes = models.CharField(max_length=200,default='')
    number = models.IntegerField(default=0)
    order_number= models.IntegerField(default=0)
    payment_gateway = models.CharField(max_length=200,default='')
    presenment_currency = models.CharField(max_length=10,default='')
    referring_site = models.CharField(max_length=200,default='')
    source_name = models.CharField(max_length=200,default='')
    total_discount = models.FloatField(default=0.0)
    total_line_item_price = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    total_line_tax = models.FloatField(default=0.0)
    total_tip = models.FloatField(default=0.0)
    user_id = models.CharField(max_length=200,default='')
    update_at = models.DateField(default=timezone.now)
    total_weight = models.CharField(max_length=20,default='')

class ClientOrder(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    accept_language = models.CharField(max_length=60,default='')
    browser_height = models.CharField(max_length=200,default='')
    browser_width = models.CharField(max_length=200,default='')
    session_hash = models.CharField(max_length=200,default='')
    user_hash = models.CharField(max_length=200,default='')


class OrderdiscountCode(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,default='')
    abandoncart_id = models.ForeignKey(AbandonCart,on_delete=models.CASCADE)    
    discount_codes = models.ForeignKey(DiscountCode,on_delete=models.CASCADE)
    discount_price = models.CharField(max_length=200,default='')
    discount_type  = models.CharField(max_length=200,default='')

class Collection(models.Model):
    body_html = models.CharField(max_length=2000,default='')
    handle = models.CharField(max_length=200,default='')
    id  = models.CharField(max_length=200,primary_key=True)
    published_at = models.DateField(default=timezone.now)
    published_scope = models.CharField(max_length=200,default='')
    sort_order = models.CharField(max_length=200,default='')
    title = models.CharField(max_length=200,default='')
    update_at = models.DateField(default=timezone.now)

class PriceRuleEntity(models.Model):
    price_rule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    collection_id = models.ForeignKey(Collection,on_delete=models.CASCADE)

class Product(models.Model):
    body_html = models.CharField(max_length=2000,default='')
    handle = models.CharField(max_length=200,default='')
    id  = models.CharField(max_length=200,primary_key=True)
    option_1=models.CharField(max_length=200,default = '')
    option_2= models.CharField(max_length=200,default = '')
    option_3 = models.CharField(max_length=200,default = '')
    product_type = models.CharField(max_length=200,default='')
    published_scope = models.CharField(max_length=200,default='')
    status = models.CharField(max_length=100,default='')
    published_date = models.DateField(default=timezone.now)
    update_at = models.DateField(default=timezone.now)
    tags = models.CharField(max_length=200,default='')
    template_suffix = models.CharField(max_length=200,default='')
    title = models.CharField(max_length=200,default='')
    vendor = models.CharField(max_length=200,default='')

class PrerequisiteProducts(models.Model):
    pricerule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)


class PriceRuleProduct(models.Model):
    price_rule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)

class ProductImage(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    id = models.CharField(max_length=200,primary_key=True)
    position = models.IntegerField(default=-1)
    src = models.CharField(max_length=200,default='')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    update_at = models.DateField(default=timezone.now)


class Collect(models.Model):
    collection_id = models.ForeignKey(Collection,on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
    position = models.IntegerField(default=-1)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    updated_at = models.DateField(default=timezone.now)


class CollectionImage(models.Model):
    collection_id = models.ForeignKey(Collection,on_delete=models.CASCADE)
    src = models.CharField(max_length=200,default='')
    alt = models.CharField(max_length=20,default='')
    created_at = models.DateField(default=timezone.now)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)


class OrderLocation(models.Model):
    lineitem_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    country_code = models.CharField(max_length=20,default='')
    province_code = models.CharField(max_length=20,default='')
    name = models.CharField(max_length=200,default='')
    address1 = models.CharField(max_length=200,default='')
    address2 = models.CharField(max_length=200,default='')
    city = models.CharField(max_length=20,default='')
    zip_code = models.CharField(max_length=20,default='')

class orderNote(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    note_name = models.CharField(max_length=20,default='')
    note_value = models.CharField(max_length=400,default='')

class orderTag(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=40,default='')
    
class ProductVariant(models.Model):
    barcode =  models.CharField(max_length=200,default='')
    compare_at_price = models.FloatField(default=0)
    fullfillment_service=  models.CharField(max_length=200,default='')
    grams =  models.FloatField(default=0.0)
    id = models.CharField(max_length=200,primary_key=True)
    image_id = models.ForeignKey(ProductImage,on_delete=models.CASCADE)
    inventory_item_id = models.CharField(max_length=200,default='')
    position =models.CharField(max_length=200,default='')
    sku = models.CharField(max_length=200,default='') 
    taxable = models.BooleanField(default=False)
    title = models.CharField(max_length=200,default='')
    updated_at = models.DateField(default=timezone.now)
    weight = models.FloatField(default=0.0)
    weight_unit = models.FloatField(max_length=10)        

class PrerequisiteVariants(models.Model):
    pricerule_id=models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    varaint_id = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)

class PriceProductVariant(models.Model):
    price_rule_id = models.ForeignKey(PriceRule,on_delete=models.CASCADE)
    product_variant_id = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)


class AbandonCartLineItem(models.Model):
    abandon_cart_id = models.ForeignKey(AbandonCart,on_delete=models.CASCADE)
    fullfillment_service = models.CharField(max_length=200,default='')
    fullfillment_status = models.CharField(max_length=200,default='')
    required_shipping = models.BooleanField(default=False)
    sku = models.CharField(max_length=200,default='')
    title = models.CharField(max_length=200,default='')
    variant_id= models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    variant_title = models.CharField(max_length=200,default='')
    vendor = models.CharField(max_length=200,default='')
class OrderLineItem(models.Model):
    fullfilment_quantity=models.CharField(max_length=200,default='')
    fullfilmen_service = models.CharField(max_length=200,default='')
    fullfilment_status = models.CharField(max_length=20,default='')
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant_id = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    vendor = models.CharField(max_length=200,default='')
    name = models.CharField(max_length=200,default='')
    gift_card = models.CharField(max_length=200,default='')
    properties = models.CharField(max_length=200,default='')
    taxable = models.BooleanField(default=False)
    tip_payment_gateway = models.CharField(max_length=20,default='')
    tip_payment_method = models.CharField(max_length=20,default='')
    total_discount_amount = models.FloatField(default=0.0)
    id = models.CharField(max_length=200,primary_key=True)