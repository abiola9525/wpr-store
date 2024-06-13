import json
import stripe

import logging
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from . models import Order, OrderItem, Product, Category
from . cart import Cart
from . forms import OrderForm
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    
    return redirect('home')

@login_required
def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    
    if action:
        quantity = 1
        
        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)
        
        return redirect('cart_view')
    
@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart = Cart(request)
    
    return render(request, 'store/cart_view.html', {
        'cart': cart
    })

'''
@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost() == 0:
        return redirect('cart_view')

    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        zipcode = data['zipcode']
        city = data['city']
        state = data['state'],
        country = data['country'],

        if first_name and last_name and address and zipcode and city and state and country:
            form = OrderForm(request.POST)
            
            total_price = 0
            items = []

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

                items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': product.price
                    },
                    'quantity': item['quantity']
                })
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url=f'127.0.0.1:8000/cart/success/',
                cancel_url=f'127.0.0.1:8000/cart/',
            )
            payment_intent = session.payment_intent

            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                zipcode=zipcode,
                city=city,
                state=state,
                country=country,
                created_by = request.user,
                is_paid = True,
                payment_intent = payment_intent,
                paid_amount = total_price
            )
            
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return JsonResponse({'session': session, 'order': payment_intent})
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })
'''

# =====================================================================================================================

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost() == 0:
        return redirect('cart_view')

    if request.method == 'POST':
        logger.debug(f'Request body: {request.body}')

        try:
            data = json.loads(request.body)
            logger.debug(f'Request body data: {data}')

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            address = data.get('address')
            zipcode = data.get('zipcode')
            city = data.get('city')
            state = data.get('state')
            country = data.get('country')

            if not all([first_name, last_name, address, zipcode, city, state, country]):
                logger.error('Missing required fields in request body')
                return HttpResponseBadRequest('Missing required fields')

            total_price = 0
            items = []

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

                items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': int(product.price * 100)  # Stripe expects amounts in cents
                    },
                    'quantity': item['quantity']
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url=request.build_absolute_uri('/cart/success/'),
                cancel_url=request.build_absolute_uri('/cart/'),
            )

            payment_intent = session.payment_intent
            if not payment_intent:
                logger.error('Payment intent not created successfully')
                return HttpResponseBadRequest('Payment intent not created')

            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                zipcode=zipcode,
                city=city,
                state=state,
                country=country,
                created_by=request.user,
                is_paid=False,
                payment_intent=payment_intent,
                paid_amount=total_price
            )

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return JsonResponse({'sessionId': session.id, 'orderId': order.id})

        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error: {e}')
            return HttpResponseBadRequest('Invalid JSON')
        except KeyError as e:
            logger.error(f'Missing field in JSON data: {e}')
            return HttpResponseBadRequest(f'Missing field: {e}')
        except stripe.error.StripeError as e:
            logger.error(f'Stripe API error: {e}')
            return HttpResponseBadRequest(f'Stripe error: {e}')
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return HttpResponseBadRequest(f'Unexpected error: {e}')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })
# ===================================================================================================================================








def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'store/search.html', {
        'query': query,
        'products': products
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    
    return render(request, 'store/product_detail.html', {
        'product': product
    })

