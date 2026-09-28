from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_application, name='submit-application'),
    path('tenant/<int:tenant_id>/', views.tenant_applications, name='tenant-applications'),
    path('landlord/<int:landlord_id>/', views.landlord_applications, name='landlord-applications'),
    path('<int:app_id>/update/', views.update_application, name='update-application'),
]