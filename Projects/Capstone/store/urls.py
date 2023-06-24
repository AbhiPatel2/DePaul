from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('store/', views.store, name="store"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', views.login, name="login"),
    path('quiz/', views.quiz, name="quiz"),
    path('cart', views.cart, name="cart"),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('', views.store, name="store"),
    path('item/<int:itemType_id>', views.item, name='item'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('warm/', views.warm, name='warm'),
    path('fruity/', views.fruity, name='fruity'),
    path('quiz_result/', views.quiz_result, name='quiz_result'),
    path('brands/', views.brands, name="brands"),
    path('brands/<brand>', views.brand, name="brands"),
    path('fragrances', views.fragrances, name="fragrances")
]

