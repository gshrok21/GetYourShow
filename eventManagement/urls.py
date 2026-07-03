"""
URL configuration for eventManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from .views import listcategories,user_api,listevent,modifyevent,Register,DownloadInvoice,CreateOrderView,VerifyPaymentView,myevent
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 



routr=routers.DefaultRouter()
routr.register("registration",Register ,basename='record')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/",user_api.as_view()),
    path("user/<int:pk>",user_api.as_view()),
    path("categories/",listcategories.as_view()),
    path('list/event/',listevent.as_view()),
    path('list/event/<slug:slug>/',modifyevent.as_view()),
    path('list/event/<slug:slug>/cancel',modifyevent.as_view()),
    path('list/event/<slug:slug>/publish',modifyevent.as_view()),
    path('/my-events/',myevent.as_view()),
    path("",include(routr.urls)),
    path('auth/token/',TokenObtainPairView.as_view()),
    path('auth/tokenrefresh/',TokenRefreshView.as_view()),
    path('generatePdf/<int:invoice_id>',DownloadInvoice.as_view()),
    path('create-order/',CreateOrderView.as_view()),
    path('verify-payment/',VerifyPaymentView.as_view())

]
