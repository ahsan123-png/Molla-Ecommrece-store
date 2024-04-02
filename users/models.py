from django.conf import settings
from django.db import models
import stripe
from django.contrib.auth.models import User
# Create your models here.
class UserEx(User):

    gender = models.CharField(max_length=10, default='unknown')
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    customer_id = models.CharField(max_length=63,null=True,blank=True)
    name = models.CharField(max_length=100, null=True)  # Nullable name field
    useraddress = models.CharField(max_length=255, null=True) 

    #set customer ID
    def set_customer_id(self):
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.api_key = 'sk_test_51NwlTxAwV6eRJVXpqA7ErOBGIDwPml63lpJhSNpwMn15qoC2EiTM36DPdVYkiyyyWyRMvnfCNI96CNn3hhty4bQ0003XqePmIT'

            try:
                customer = stripe.Customer.create(
                    phone=self.phone,
                    email=self.email,
                    name=self.get_full_name(),
                )
                self.customer_id = customer.id
                self.save()
            except stripe.error.StripeError as e:
                # Handle any Stripe-related errors here
                # You may want to log the error or take other actions as needed
                # For example: print(f"Stripe Error: {e}")
                pass
    


    #set a function to clean phone no
    def set_phone(self,phone):
        if phone.__contains__(""):
            phone.replace(" ","")
        if phone.__contains__("-"):
            phone.replace("-","")
        if phone.__contains__("+"):
            phone.replace("+","")
        self.phone=phone
        self.save()

    def phone_number(self):
        return f"+{self.phone_no}"
    
# ==== contact model ====
class Contact(models.Model):
    cusName=models.CharField(max_length=50)
    cusEmail=models.EmailField(max_length=255,
                                unique=False,
                                blank=False,
                                null=False,)
    cusPhone=models.CharField(max_length=50,null=False,blank=False)
    cusSubject=models.CharField(max_length=100,blank=False,null=False)
    cusMessage=models.CharField(max_length=300,blank=False,null=False)