"""zadanie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from django_registration.backends.activation.views import RegistrationView
from users.forms import CustomUserForm


urlpatterns = [
    path('', TemplateView.as_view(template_name = "home.html"), name = 'home'),
    path(
        'accounts/register/',
        RegistrationView.as_view(
            form_class=CustomUserForm
        ),
        name='django_registration_register',
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/signup/', RegistrationView.as_view(), name='registration_view'),
    #path('accounts/', include('allauth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace = 'articles')),
    path('blog/', include('blog.urls', namespace = 'blog')),
    path('search/', include('haystack.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
