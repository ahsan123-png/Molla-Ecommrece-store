from django.urls import reverse
from pyexpat.errors import messages

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
# from django.shortcuts import render
import stripe
# from stripe import Card, Order 
from django.conf import settings
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from product.models import Product
from users.models import UserEx
stripe.api_key = settings.STRIPE_SECRET_KEY
# #=========================================
stripe.api_key = 'sk_test_51NwlTxAwV6eRJVXpqA7ErOBGIDwPml63lpJhSNpwMn15qoC2EiTM36DPdVYkiyyyWyRMvnfCNI96CNn3hhty4bQ0003XqePmIT'  # Replace with your Stripe secret key
# #-------->Card info<----------
def payment(request):
    if request.method == "POST":
        subtotal = request.POST.get("initial_subtotal")
        subtotal = float(subtotal)
        user = request.user
        try:
            user_ex = UserEx.objects.get(id=user.id)
        except UserEx.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('fail')

        credit_card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv_code = request.POST.get('cvv')
        exp_date_parts = expiry_date.split('/')
        if len(exp_date_parts) != 2:
            return HttpResponseRedirect(reverse('checkout'))

        # Prepare card information for Stripe
        card_info = {
            "number": credit_card_number,
            "exp_month": int(exp_date_parts[0]),
            "exp_year": int(exp_date_parts[1]),
            "cvc": cvv_code,
        }

        # Create a PaymentMethod using the card info
        try:
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=card_info
            )
        except stripe.error.CardError as e:
            print(f"Card error: {e}")
            return redirect('fail')
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return redirect('fail')

        # Create a PaymentIntent with the PaymentMethod
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(subtotal * 100),
                currency="usd",
                customer=user_ex.customer_id,
                payment_method=payment_method.id,
                confirm=True
            )
        except stripe.error.CardError as e:
            print(f"Card error: {e}")
            return redirect('fail')
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return redirect('fail')

        if payment_intent.status == 'succeeded':
           return redirect("success")
        else:
            return redirect("fail")

def success(request):
    return render(request,"success.html")


def failed(request):
    return render(request,"failed.html")