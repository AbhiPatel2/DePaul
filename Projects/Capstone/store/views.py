from __future__ import annotations
import json
from warnings import catch_warnings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import store.models as models
import store.interaction as interaction
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse
from store.Cart import Cart, CartItem 
from .forms import QuizForm
from .questions import questions
import pprint
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def loggedIn(request: HttpRequest):
    return request.user.is_authenticated
    

def login(request: HttpRequest):
    context = {}
    return render(request, 'registration/login.html', context)

    # verification = interaction.loginVerify(request.POST['username'], request.POST['password'])
    # if verification[0] == Status.SUCCESS:
    #     request.session['member_id'] = verification[1].id
    #     return HttpResponse("logged in")
    # else:
    #     return HttpResponse(verification[1])

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def cart(request: HttpRequest):
    #del request.session['cart']
    context = {}
    #if (not loggedIn(request)):
    #    return render(request, 'registration/login.html', context)
    # print(f"ii={item_id}")
    cart = request.session.get('cart', Cart())
    # cart.item_count = 0
    # if(len(cart.items) <= 0):
    #     cart.item_count = 0
    #     itemType = models.ItemType.objects.last()
    #     item_id = str(itemType.id)
    #     print("addd fake 1")
    #     cart.cart_add(item_id)
        
    id = request.POST.get("add_cart_item_id", None)
    if not(id is None ) and (id != ""):
        itemType = get_object_or_404(models.ItemType, id=id)
        item_id = str(itemType.id)
        cart.cart_add(item_id)
    id = request.POST.get("remove_cart_item_id", None)
    if not(id is None) and (id != ""):
        itemType = get_object_or_404(models.ItemType, id=id)
        item_id = str(itemType.id)
        cart.cart_remove(item_id)
        
    request.session['cart'] = cart
    context={
        'cart': cart.items,
        'cart_item_count': cart.item_count,
        'cart_grandTotal':cart.grandTotal
        
        }
    print(cart)
    return render(request, 'store/cart.html', context)

@require_POST
def add_to_cart(request: HttpRequest):
    context = {}
    #if (not loggedIn(request)):
    #    return render(request, 'registration/login.html', context)
    cart = request.session.get('cart', Cart())
    id = request.POST.get("id", None)
    if not(id is None ) and (id != ""):
        itemType = get_object_or_404(models.ItemType, id=id)
        item_id = str(itemType.id)
        cart.cart_add(item_id)
        print(cart)
    request.session['cart'] = cart
    return HttpResponse('success')

def checkout(request: HttpRequest):
    context = {}
    #if (not loggedIn(request)):
    #    return render(request, 'registration/login.html', context)
    cart = request.session.get('cart', Cart())
    context['cart_item_count']= cart.item_count()
    return render(request, 'store/checkout.html', context)


def centsToStr(cents: int) -> str:
    actualCents = cents % 100
    price = str(cents // 100)
    if actualCents != 0:
        if actualCents < 10:
            actualCents = str(actualCents) + "0"
        price = "{}.{}".format(price, actualCents)
    return price


converter = lambda it: (it, {'brand': it.brand.name, 'image': it.image,'category': it.category.name,
                             'price': centsToStr(it.priceCents), 'sale': centsToStr(it.salePrice)})

def itemsToDict(items: list[models.ItemType]):
    return dict(list(map(converter, items)))


def getCartNumber(request: HttpRequest):
    context = {}
    cart = request.session.get('cart', Cart())
    context['cart_item_count']= cart.item_count()
    #if (not loggedIn(request)):
    #    return 0
    #else:
        #return context
    return request.session.get('cart').item_count


def store(request: HttpRequest):

    # buyitagain_items = if (request.)
    cart = request.session.get('cart', Cart())

    context = {
        'bestseller_items': itemsToDict([i.itemType for i in models.BestSellers.objects.all() if i.itemType.quantity > 0]),
        'newarrivals_items': itemsToDict([i.itemType for i in models.NewArrivals.objects.all() if i.itemType.quantity > 0]),
        # 'buyitagain_items': itemsToDict(buyitagain_items)
        'cart_item_count': cart.item_count()
    }
    return render(request, 'store/store.html', context)


def item(request: HttpRequest, itemType_id):
    item = models.ItemType.objects.get(pk=itemType_id)  # primary key
    cart = request.session.get('cart', Cart())
    context = {
        'item': item,
        'cart_item_count': cart.item_count()
    }
    return render(request, 'store/item.html', context)


def thank_you(request):
    context = {}
    return render(request, 'store/thank_you.html', context)


def fruity(request):
    context = {}
    return render(request, 'store/fruity.html', context)


def warm(request):
    context = {}
    return render(request, 'store/warm.html', context)


def quiz(request: HttpRequest):
    cart = request.session.get('cart', Cart())
    context = {
        'cart_item_count': cart.item_count(),
        'questions': questions,
        'form': QuizForm()
    }
    return render(request, 'store/quiz.html', context)


def quiz_result(request: HttpRequest):
    print(request.POST)
    form = QuizForm(request.POST)
    cart = request.session.get('cart', Cart())
    if form.is_valid():
        # answer = form.clean()
        
        # valA_answers = len(answer['valA_answer'])
        # valB_answers = len(answer['valB_answer'])

        # print(valA_answers)
        # print(valB_answers)
        # Do something with the correct answers

        #if valA_answers > valB_answers:
        #   result = ' You are an A person'
        #else:
        #   result ='You are an B person'
            #Answer 1 has more correct answers
        #  return render(request, 'fruity.html', {'result': 'Based on your answers, you would enjoy the fresh, fruity, and floral fragrances.'})
        #else:
        #   return render(request, 'warm.html', {'result': 'Based on your answers, you would enjoy the woody and warm fragrances'})

        # ...

    # call this:    interaction.getCorrelations()

        context = {
            #'cart_item_count': cart.item_count(),
            'form': form,
            #'valA_answers': valA_answers,
            #'valB_answers': valB_answers,
        }
        return render(request, 'store/quiz_result.html', context)
    print(form.errors)


def brands(request: HttpRequest):
    cart = request.session.get('cart', Cart())
    available_brands = dict(list(map(
        lambda it: (it, {'image': it.logoImage}),  
        [brand for brand in models.Brand.objects.all()]
    )))
    
    context = {
        'cart_item_count': cart.item_count(),
        'available_brands': available_brands}
    return render(request, 'store/brands.html', context)


def brand(request: HttpRequest, brand):
    brandItems: list[models.ItemType] = models.ItemType.objects.filter(brand__name__iexact=brand).all()
    print(brandItems)
    # if len(brandItems) == 0:
    cart = request.session.get('cart', Cart())
    context = {
        'cart_item_count': cart.item_count(),
        'brand_name': brand,
        'brand_items': itemsToDict(brandItems)
    }
    return render(request, 'store/brand.html', context)


def fragrances(request: HttpRequest):
    cart = request.session.get('cart', Cart())
    context = {
        'cart_item_count': cart.item_count(),
        'all_items': itemsToDict([i for i in models.ItemType.objects.all()])
    }

    return render(request, 'store/fragrances.html', context)
