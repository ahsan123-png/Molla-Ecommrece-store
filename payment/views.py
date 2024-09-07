from django.urls import reverse
from pyexpat.errors import messages

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
# from django.shortcuts import render
import stripe
# from stripe import Card, Order 
from django.conf import settings
from order.models import Order, ShipmentAddress
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from product.models import Product
from users.models import UserEx
stripe.api_key = settings.STRIPE_SECRET_KEY
# #=========================================

# #-------->Card info<----------
def payment(request):
    if request.method == "POST":
        subtotal = request.POST.get("initial_subtotal")
        if not subtotal:
            messages.error(request, 'Subtotal is missing.')
            return redirect('fail')
        try:
            subtotal = float(subtotal)
        except ValueError:
            messages.error(request, 'Invalid subtotal value.')
            return redirect('fail')
        user = request.user
        try:
            user_ex = UserEx.objects.get(id=user.id)
        except UserEx.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('fail')
        stripe_token = request.POST.get('stripeToken')
        if not stripe_token:
            messages.error(request, 'Missing Stripe token.')
            return redirect('fail')
        if not user_ex.customer_id:
            try:
                user_ex.set_customer_id()
            except Exception as e:
                print(f"Error creating customer: {e}")
                messages.error(request, 'Failed to create Stripe customer.')
                return redirect('fail')
        if not user_ex.customer_id:
            messages.error(request, 'Stripe customer ID not found.')
            return redirect('fail')
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(subtotal * 100),  # Convert to cents
                currency="usd",
                payment_method_data={
                    "type": "card",
                    "card": {
                        "token": stripe_token  # Use the token in card[token]
                    }
                },
                customer=user_ex.customer_id,
                confirm=True,
                return_url=request.build_absolute_uri(reverse('success'))
            )
        except stripe.error.CardError as e:
            print(f"Card error: {e}")
            return redirect('fail')
        except stripe.error.RateLimitError as e:
            print(f"Rate limit error: {e}")
            return redirect('fail')
        except stripe.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
            return redirect('fail')
        except stripe.error.AuthenticationError as e:
            print(f"Authentication error: {e}")
            return redirect('fail')
        except stripe.error.APIConnectionError as e:
            print(f"API connection error: {e}")
            return redirect('fail')
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return redirect('fail')
        except Exception as e:
            print(f"Something went wrong: {e}")
            return redirect('fail')

        if payment_intent.status == 'succeeded':
            return redirect("success")
        else:
            return redirect("fail")
    else:
        return redirect("fail")

def success(request):
    if request.method == "GET":
        user=request.user
        if isinstance(user,UserEx):
            userEx=user
        else:
            userEx=UserEx.objects.get(id=user.id)
        latest_order=Order.objects.filter(customer=userEx).order_by("-id").first()
        shipment_address=ShipmentAddress.objects.filter(customer=userEx).order_by("-id").first()
        context={

            "latest_order" : latest_order,
            "shipment_address" :shipment_address
        }

    return render(request,"success.html", context)


def failed(request):
    return render(request,"failed.html")