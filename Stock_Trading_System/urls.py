"""Stock_Trading_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from Transaction_Client import views as Transaction_Client_views
from search import views as search_views

urlpatterns = [
    # url(r'^$', 'login.views.index', name='login'),
    #example
    url(r'^admin/', admin.site.urls),
    #Transaction Client
    url(r'^TransactionClient/', Transaction_Client_views.login),
    #search
    url(r'^search/',search_views.main),
    url(r'^r1min', search_views.refresh_1min),
    url(r'^r5s', search_views.refresh_5s),
    url(r'^shr', search_views.search_history),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
