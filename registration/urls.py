from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('register',views.register, name="register"),
    path('addFavorite',views.addToFavorite, name="home"),
    path('delFavView',views.delFavView, name="home"),
    path('login',views.login, name="login"),
    path('logout',views.logout, name="logout"),
    path('RenderUserSettings',views.RenderUserSettings, name="userSettings"),#for now just log out need to design user settings page
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('jCoin/',views.JsonObjectView.as_view(), name="jCoin"),
    path('jFav/', views.JsonFavoriteView.as_view(), name='jFav'),
    path('delFav/', views.DeleteFromFavApi.as_view(), name='delFav'),
    path('addFav/', views.AddToFavAPI.as_view(), name='addFav'),
    path('',views.home,name="home")
]
