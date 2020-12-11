from django.urls import path, include
from . import views

app_name = "listings"
urlpatterns = [
    path('', views.index_view, name="index"),
    path("get-xml/", views.get_xml, name="get_xml"),
    path('add-listing/', views.create_listing_view, name="newlisting"),
    path('listings/', views.ListingsView.as_view(), name="listings_list"),
    path('listings/<slug:slug>/', views.handle_property_detail_and_contact, name='listing_detail'),
    path('delete-property/<slug:slug>/', views.PropertyDelete.as_view(), name="delete_property"),
    path('update-property/<slug:slug>/', views.PropertyUpdate.as_view(), name="update_property"),
]
