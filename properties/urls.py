from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property-list'),
    path('<int:property_id>/', views.property_detail, name='property-detail'),
    path('landlord/<int:landlord_id>/', views.landlord_properties, name='landlord-properties'),
    path('stats/summary/', views.property_stats, name='property-stats'),
    path('export/csv/', views.export_csv, name='export-csv'),
]