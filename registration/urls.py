from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django_email_verification import urls as email_urls

urlpatterns = [
     path('register', views.register, name="register"),
     path('addFavorite', views.addToFavorite, name="addFavorite"),
     path('delFavorite', views.delFavView, name="deleteFavorite"),
     path('details/<str:value>', views.crypto_details, name="details"),
     path('login', views.login, name="login"),
     path('logout', views.logout, name="logout"),
     path('changeFavCurrency', views.changeFavCurrency, name="changeCurrency"),
     path('filter', views.filter, name='home'),
     path('stock',views.stock, name='stock'),
     path('notificationTab', views.notificationTab, name="notificationTab"),
     path('modifyNotification', views.modifyNotification, name="modifyNotification"),
     path('createNotification', views.createNotification, name="CreateNotification"),
     path('deleteNotification', views.deleteNotification, name="deleteNotification"),
     path('changeNotification', views.changeNotification, name="changeNotification"),
     path('stockTickFinder',views.stockTickFinder,name='stockTickFinder'),
     path('email/', include(email_urls)),
     path('', views.home, name="home"),

#     API
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
     path('changeCurrency/', views.ChangeCurrencyFav.as_view()),
     path('coins/', views.JsonObjectView.as_view()),
     path('coins/<str:id>', views.AllCoinInformation.as_view()),
     path('favorites/', views.JsonFavoriteView.as_view()),
     path('favorites/delete', views.DeleteFromFavApi.as_view()),
     path('favorites/add', views.AddToFavAPI.as_view()),
     path('notifications/change', views.changeEnabledNoti.as_view()),
     path('notifications/create', views.CreateNotificationApi.as_view()),
     path('notifications/delete', views.DeleteNotificationApi.as_view()),
     path('notifications/', views.UserNotifications.as_view()),
]
