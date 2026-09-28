from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def serve_page(template_name):
    def view(request):
        return render(request, f'pages/{template_name}')
    return view


urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/accounts/',     include('accounts.urls')),
    path('api/properties/',   include('properties.urls')),
    path('api/applications/', include('applications.urls')),

    path('property-detail/',     serve_page('property-detail.html')),
    path('add-property/',        serve_page('add-property.html')),
    path('edit-property/',       serve_page('edit-property.html')),
    path('manage-applications/', serve_page('manage-applications.html')),
    path('applications/',        serve_page('applications.html')),
    path('properties/',          serve_page('properties.html')),
    path('dashboard/',           serve_page('dashboard.html')),
    path('register/',            serve_page('register.html')),
    path('profile/',             serve_page('profile.html')),
    path('stats/',               serve_page('stats.html')),
    path('login/',               serve_page('login.html')),
    path('',                     serve_page('index.html')),
]