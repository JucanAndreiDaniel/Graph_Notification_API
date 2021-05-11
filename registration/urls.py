from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.conf import settings
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('addFavorite', views.addToFavorite, name="addFavorite"),
    path('delFavorite', views.delFavView, name="deleteFavorite"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('userSettings', views.userSettings, name="userSettings"),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('jCoin/', views.JsonObjectView.as_view(), name="jCoin"),
    path('jFav/', views.JsonFavoriteView.as_view(), name='jFav'),
    path('cryptoSpecific/<str:id>', views.CryptoSpecificView.as_view()),
    path('delFav/', views.DeleteFromFavApi.as_view(), name='delFav'),
    path('addFav/', views.AddToFavAPI.as_view(), name='addFav'),
    path('changeCurrency/', views.ChangeCurrencyFav.as_view(), name='changecurrency'),
    path('filter', views.filter, name='home'),
    path('base', views.base),
    path('notificationTab',views.notificationTab,name="notificationTab"),
    path('createNotification', views.createNotification, name="CreateNotification"),
    path('', views.home, name="home"),
]
