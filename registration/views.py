from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import PermissionsMixin, User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
import json
# Rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import cryptoObject, Profile, value, Notification

from django.db.models import F, Q

from django.views.generic.list import ListView

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


# Serializare Obiect Crypto in json
class JsonObjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':
            user = User.objects.filter(username=request.user.username).get()
            profile = Profile(user=user)
            values = list(cryptoObject.objects.annotate(current=F("value__current"), high_1d=F("value__high_1d"), low_1d=F("value__low_1d"), currency=F("value__currency")).values(
                "name", "current", "high_1d", "low_1d").filter(Q(currency=profile.fav_currency)))
            # value.objects.values_list(
            #     "name","current", "high_1d", "low_1d").filter(currency="usd").filter(
            #     coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))
            return JsonResponse(values, safe=False)

# Serializare Favorite in functie de user

from django.shortcuts import get_object_or_404
class JsonFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':
            user = User.objects.filter(username=request.user.username).get()
            profile = Profile(user=user)
            favorites = list(profile.favorite.annotate(current=F("value__current"), high_1d=F("value__high_1d"), low_1d=F("value__low_1d"), currency=F("value__currency")).values(
                "name", "current", "high_1d", "low_1d").filter(Q(currency=profile.fav_currency)))
            return JsonResponse(favorites, safe=False)


# Returns data from crypto coin based on its id
class CryptoSpecificView(ListView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,**kwargs):
        user = get_object_or_404(User.objects.filter(username=request.user.username))
        values = get_object_or_404(cryptoObject.objects.annotate(current=F("value__current"), high_1d=F("value__high_1d"), low_1d=F("value__low_1d"), currency=F("value__currency")).values(
                 "name", "current", "high_1d", "low_1d").filter(Q(currency=user.profile.fav_currency)).filter(coin_id=kwargs.get('id')))
        return JsonResponse(values,safe=False)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            messages.info(request, 'Invalid username or password.')
            return HttpResponseRedirect('login')
    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        get_name = request.POST['get_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=user_name, password=password1, email=email, get_name=get_name, last_name=last_name)
                user.save()
                messages.success(
                    request, f'Account was created for {user.username}')
                return redirect('login')

        else:
            messages.info(request, 'password not matching..')
            return redirect('register')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url="login")
def home(request):
    # base(request)
    dic = checkPrices(request)
    createProfileFromUserID(request.user.id)
    currency = Profile.objects.get(user_id=request.user.id)
    currency = currency.fav_currency
    prices = value.objects.filter(currency=currency)
    page = request.GET.get('page', 1)
    favorites = value.objects.filter(currency=currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))
    paginator = Paginator(prices, 30)
    try:
        price = paginator.page(page)
    except PageNotAnInteger:
        price = paginator.page(1)
    except EmptyPage:
        price = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"crypto": price, "fav": favorites, "notificare": dic})


def filter(request):
    currency = Profile.objects.get(user_id=request.user.id)
    currency = currency.fav_currency
    contain = request.GET.get('contain')
    if(contain == ""):
        return home(request)
    prices = cryptoObject.objects.annotate(current=F("value__current"), high_1d=F("value__high_1d"), low_1d=F(
        "value__low_1d"), currency=F("value__currency")).filter(Q(currency=currency)).filter(coin_id__contains=contain)
    page = request.GET.get('page', 1)
    favorites = value.objects.filter(currency=currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))
    paginator = Paginator(prices, 10)
    try:
        price = paginator.page(page)
    except PageNotAnInteger:
        price = paginator.page(1)
    except EmptyPage:
        price = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"crypto": price, "fav": favorites})


def base(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    dic = checkPrices(request)
    print(dic)
    return render(request, 'base.html', {user: user, 'vapid_key': vapid_key, "notificare": dic})


def createProfileFromUserID(id):
    try:
        profile = Profile.objects.create(user_id=id)
    except:
        pass


def addToFav(user, crypto_id):
    profile = Profile(user=user)
    crypto_add = cryptoObject.objects.get(
        coin_id=crypto_id)
    profile.save()
    profile.favorite.add(crypto_add)
    profile.save()
    return


def addToFavorite(request):
    if request.method == 'POST':
        # request form html the name of crypto to be added to favorites
        add_favorite = request.POST["crypto.id"][:-4]
        # the name of user who requested a favorite crypto
        user = User.objects.filter(username=request.user.username).get()
        addToFav(user, add_favorite)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddToFavAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == "POST":
            add_favorite = request.data.get("crypto_id")
            user = User.objects.filter(username=request.user.username).get()
            addToFav(user, add_favorite)
            return Response("Added")


def deleteFav(user, crypto_id):
    # user defines what type of currency does he want to be added later :)
    crypto_delete = cryptoObject.objects.filter(
        coin_id=crypto_id).get()
    profile = Profile(user=user)
    profile.favorite.remove(crypto_delete)
    profile.save()
    return


@require_http_methods(["POST"])
def delFavView(request):
    # request form html the name of crypto to be added to favorites
    delete_favorite = request.POST["crypto.id"][:-4]
    # the name of user who requested a favorite crypto
    user = User.objects.filter(username=request.user.username).get()
    deleteFav(user, delete_favorite)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromFavApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            delete_favorite = request.data.get("crypto_id")
            print(delete_favorite)
            user = User.objects.filter(username=request.user.username).get()
            deleteFav(user, delete_favorite)
            return Response("Deleted")


@login_required(login_url="login")
def userSettings(request):
    cList = ["usd", "eur", "rub", "gbp"]
    user = Profile.objects.get(user_id=request.user.id)
    favorites = value.objects.filter(currency=user.fav_currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))
    if request.method == 'POST':
        favoriteCurrency = request.POST['curr']
        user.fav_currency = favoriteCurrency
        user.save()
        return HttpResponseRedirect('userSettings')
    cList.remove(user.fav_currency)
    return render(request, 'userSettings.html', {"currencyList": cList, "favC": user.fav_currency, "fav": favorites})


def createNotification(request):

    user = Profile.objects.get(user__id=request.user.id)
    coin_result = cryptoObject.objects.get(
        coin_id=request.POST.get('crypto.id'))
    option = request.POST.get('option')
    crypto_value = float(request.POST.get('crypto.value'))
    final_value = float(request.POST.get('value'))

    if final_value < 0:
        messages.info(request, 'Requested value is negative')
        return HttpResponseRedirect('userSettings')
    if option == "g_perc":
        final_value = crypto_value + (crypto_value * final_value)/100
    elif option == "d_perc":
        if final_value >= 100:
            messages.info(request, 'Requested value is invalid')
            return HttpResponseRedirect('userSettings')
        final_value = crypto_value - (crypto_value * final_value)/100
    else:
        final_value = crypto_value

    notificare = Notification(user=user, coin=coin_result,
                              value_type=option, intial_value=crypto_value, final_value=final_value)
    notificare.save()

    return HttpResponseRedirect('userSettings')


def checkPrices(request):
    user = Profile.objects.get(user_id=request.user.id)
    notification_coins = Notification.objects.filter(user_id=request.user.id)
    user1 = User.objects.filter(username=request.user.username).get()
    profile = Profile(user=user1)
    print(notification_coins)

    favorites = value.objects.filter(currency=user.fav_currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))

    dic = {}
    for noti in notification_coins:
        for fav in favorites:
            if noti.coin.coin_id == fav.coin.coin_id:
                # for testing change fav.current
                if noti.final_value == fav.current:
                    dic[noti.coin.coin_id] = noti.final_value
    js_data = json.dumps(dic)
    return js_data


class ChangeCurrencyFav(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            favorite_currency = request.data.get("favorite_currency")
            user = Profile.objects.get(user__id=request.user.id)
            user.fav_currency = favorite_currency
            user.save()
            return Response("Favorite currency updated")
