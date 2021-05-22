from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('register', views.register, name="register"),
    path('addFavorite', views.addToFavorite, name="addFavorite"),
    path('delFavorite', views.delFavView, name="deleteFavorite"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('userSettings', views.userSettings, name="userSettings"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('coins/', views.JsonObjectView.as_view(), name="jCoin"),
    path('favorites/', views.JsonFavoriteView.as_view(), name='jFav'),
    path('coin/<str:id>', views.AllCoinInformation.as_view()),
    path('delFav/', views.DeleteFromFavApi.as_view(), name='delFav'),
    path('addFav/', views.AddToFavAPI.as_view(), name='addFav'),
    path('changeCurrency/', views.ChangeCurrencyFav.as_view(), name='changecurrency'),
    path('filter', views.filter, name='home'),
    path('base', views.base),
    path('stock',views.stock, name='stock'),
    path('notificationTab', views.notificationTab, name="notificationTab"),
    path('modifyNotification', views.modifyNotification, name="modifyNotification"),
    path('changeEnabledNoti', views.changeEnabledNoti.as_view(),
         name="changeEnabledNoti"),
    path('createNotification', views.createNotification, name="CreateNotification"),
    path('createNotificationApi', views.CreateNotificationApi.as_view(),
         name="createNotificationApi"),
    path('deleteNotification', views.deleteNotification, name="deleteNotification"),
    path('deleteNotificationApi', views.DeleteNotificationApi.as_view(),
         name="deleteNotificationApi"),
    path('changeNotification', views.changeNotification, name="changeNotification"),
    path('changeNotificationApi', views.changeNotificationApi.as_view(),
         name="changeNotificationApi"),
    path('email/', include(email_urls)),
    path('notifications/', views.UserNotifications.as_view()),
    path('', views.home, name="home"),
]
