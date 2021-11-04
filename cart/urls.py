from django.urls import path
from . import views

urlpatterns = [
    path("add-to-cart/", views.AddtoCart.as_view(), name="add_to_cart"),
    path("remove-from-cart/<id>/",views.RemoveFromCart.as_view(),name="remove_from_cart"),
    path("remove-item-direct/<id>/", views.RemoveItemDirect.as_view(), name="remove_direct"),
    path("get-cart-items/<email>/", views.GetCartItems.as_view(), name="get_items_cart"),
    
]
