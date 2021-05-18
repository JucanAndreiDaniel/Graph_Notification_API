from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django_email_verification import send_email
import json
# Rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import cryptoObject, Profile, value, Notification

from django.db.models import F, Q


# Serializare Obiect Crypto in json
class JsonObjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get('currency') is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get('currency')

            values = list(cryptoObject.objects
                          .annotate(current=F("value__current"),
                                    high_1d=F("value__high_1d"),
                                    low_1d=F("value__low_1d"),
                                    currency=F("value__currency"),
                                    ath=F("value__ath"),
                                    ath_time=F("value__ath_time"),
                                    atl=F("value__atl"),
                                    atl_time=F("value__atl_time"))
                          .values("coin_id",
                                  "symbol",
                                  "name",
                                  "image",
                                  "last_updated",
                                  "current",
                                  "high_1d",
                                  "low_1d",
                                  "ath",
                                  "ath_time",
                                  "atl",
                                  "atl_time")
                          .filter(Q(currency=currency)))

            return JsonResponse(values, safe=False)

# Serializare Favorite in functie de user


class JsonFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get('currency') is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get('currency')

            favorites = list(user.favorite
                             .annotate(current=F("value__current"),
                                       high_1d=F("value__high_1d"),
                                       low_1d=F("value__low_1d"),
                                       currency=F("value__currency"),
                                       ath=F("value__ath"),
                                       ath_time=F("value__ath_time"),
                                       atl=F("value__atl"),
                                       atl_time=F("value__atl_time"))
                             .values("coin_id",
                                     "symbol",
                                     "name",
                                     "image",
                                     "last_updated",
                                     "current",
                                     "high_1d",
                                     "low_1d",
                                     "ath",
                                     "ath_time",
                                     "atl",
                                     "atl_time")
                             .filter(Q(currency=currency)))

            return JsonResponse(favorites, safe=False)


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
        first_name = request.POST['first_name']
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
                    username=user_name, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()
                send_email(user)
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
    createProfileFromUserID(request.user.id)
    user = Profile.objects.get(user__id=request.user.id)
    lista = checkPrices(request)
    dic = lista[0]
    currency = Profile.objects.get(user__id=request.user.id)
    currency = currency.fav_currency
    prices = cryptoObject.objects.annotate(current=F("value__current"),
                                    high_1d=F("value__high_1d"),
                                    low_1d=F("value__low_1d"),
                                    currency=F("value__currency"),
                                    ath=F("value__ath"),
                                    ath_time=F("value__ath_time"),
                                    atl=F("value__atl"),
                                    atl_time=F("value__atl_time")).values("coin_id",
                                  "symbol",
                                  "name",
                                  "image",
                                  "last_updated",
                                  "current",
                                  "high_1d",
                                  "low_1d",
                                  "ath",
                                  "ath_time",
                                  "atl",
                                  "atl_time").filter(Q(currency=currency))
    page = request.GET.get('page', 1)
    favorites = user.favorite.annotate(current=F("value__current"),
                                       high_1d=F("value__high_1d"),
                                       low_1d=F("value__low_1d"),
                                       currency=F("value__currency"),
                                       ath=F("value__ath"),
                                       ath_time=F("value__ath_time"),
                                       atl=F("value__atl"),
                                       atl_time=F("value__atl_time")).values("coin_id",
                                     "symbol",
                                     "name",
                                     "image",
                                     "last_updated",
                                     "current",
                                     "high_1d",
                                     "low_1d",
                                     "ath",
                                     "ath_time",
                                     "atl",
                                     "atl_time").filter(Q(currency=currency))
    paginator = Paginator(prices, 30)
    try:
        price = paginator.page(page)
    except PageNotAnInteger:
        price = paginator.page(1)
    except EmptyPage:
        price = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"crypto": price, "fav": favorites, "notificare": dic, "nrnot": lista[1]})


def filter(request):
    lista = checkPrices(request)
    dic = lista[0]
    currency = Profile.objects.get(user__id=request.user.id)
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
    return render(request, 'home.html', {"crypto": price, "fav": favorites, "notificare": dic,"nrnot": lista[1]})


def base(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    dic = checkPrices(request)
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
        add_favorite = request.POST["crypto.id"]
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
    delete_favorite = request.POST["crypto.id"]
    print(delete_favorite)
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
    lista = checkPrices(request)
    dic = lista[0]
    cList = ["usd", "eur", "rub", "gbp"]
    user = Profile.objects.get(user__id=request.user.id)
    favorites = user.favorite.annotate(current=F("value__current"),
                                       high_1d=F("value__high_1d"),
                                       low_1d=F("value__low_1d"),
                                       currency=F("value__currency"),
                                       ath=F("value__ath"),
                                       ath_time=F("value__ath_time"),
                                       atl=F("value__atl"),
                                       atl_time=F("value__atl_time")).values("coin_id",
                                     "symbol",
                                     "name",
                                     "image",
                                     "last_updated",
                                     "current",
                                     "high_1d",
                                     "low_1d",
                                     "ath",
                                     "ath_time",
                                     "atl",
                                     "atl_time").filter(Q(currency=user.fav_currency))
    if request.method == 'POST':
        favoriteCurrency = request.POST['curr']
        user.fav_currency = favoriteCurrency
        user.save()
        return HttpResponseRedirect('userSettings')
    cList.remove(user.fav_currency)
    return render(request, 'userSettings.html', {"currencyList": cList, "favC": user.fav_currency, "fav": favorites, "notificare": dic,"nrnot": lista[1]})


@login_required(login_url="login")
def notificationTab(request):
    
    lista = checkPrices(request)
    dic = lista[0]
    currency = Profile.objects.get(user__id=request.user.id)
    currency = currency.fav_currency
    user = Profile.objects.get(user__id=request.user.id)
    favorites = user.favorite.annotate(current=F("value__current"),
                                       high_1d=F("value__high_1d"),
                                       low_1d=F("value__low_1d"),
                                       currency=F("value__currency"),
                                       ath=F("value__ath"),
                                       ath_time=F("value__ath_time"),
                                       atl=F("value__atl"),
                                       atl_time=F("value__atl_time")).values("coin_id",
                                     "symbol",
                                     "name",
                                     "image",
                                     "last_updated",
                                     "current",
                                     "high_1d",
                                     "low_1d",
                                     "ath",
                                     "ath_time",
                                     "atl",
                                     "atl_time").filter(Q(currency=currency))
                                         
    notification_coins = Profile.objects.get(
        user__id=request.user.id).notification.all()
    print(notification_coins)
    return render(request, 'notificationTab.html', {"favorites":favorites,"notificari": notification_coins,"notificare": dic,"nrnot": lista[1]})


def modifyNotification(request):
    if request.method == 'POST':
        noti_disable = Profile.objects.get(
                    user__id=request.user.id).notification.get(coin_id = request.POST.get('crypto_id'))
        noti_disable.enabled= bool(request.POST.get('state'))
        noti_disable.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def createNotification(request):
    user = Profile.objects.get(user__id=request.user.id)
    coin_result = cryptoObject.objects.get(
        coin_id=request.POST.get('optionCrypto').lower())
    option = request.POST.get('option')
    crypto_value = cryptoObject.objects.annotate(current=F("value__current"),currency=F("value__currency"),
                                ).values("current","currency").filter(Q(currency=user.fav_currency)).get(coin_id=request.POST.get('optionCrypto').lower())
    crypto_value = crypto_value['current']
    final_value = float(request.POST.get('value'))
    if final_value < 0:
        return HttpResponseRedirect('userSettings')
    if option == "g_perc":
        final_value = crypto_value + (crypto_value * final_value)/100
    elif option == "d_perc":
        if final_value >= 100:
            return HttpResponseRedirect('userSettings')
        final_value = crypto_value - (crypto_value * final_value)/100
    else:
        final_value = final_value

    notificare = Notification(coin=coin_result,
                              value_type=option, intial_value=crypto_value, final_value=final_value)
    notificare.save()
    user.notification.add(notificare)
    user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deleteNotification(request):
    noti_delete = Profile.objects.get(
                    user__id=request.user.id).notification.get(coin_id = request.POST.get('crypto_delete'))
    noti_tabela_mare = Notification.objects.get(id = noti_delete.id).delete()
    profile = Profile(user=request.user)
    profile.notification.remove(noti_delete)
    profile.save()
    print(noti_delete)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkPrices(request):
    user = Profile.objects.get(user__id=request.user.id)
    notification_coins = user.notification.all()

    favorites = value.objects.filter(currency=user.fav_currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id))

    dic = {}
    for noti in notification_coins:
        if noti.enabled == 1:
            for fav in favorites:
                if noti.coin.coin_id == fav.coin.coin_id:
                    # for testing change fav.current
                    if noti.value_type == "bigger":
                        if fav.current > noti.final_value:
                            dic[noti.coin.coin_id] = fav.current
                    elif noti.value_type == "lower":
                        if fav.current < noti.final_value:
                            dic[noti.coin.coin_id] = fav.current
                    else:
                        if noti.final_value == fav.current:
                            dic[noti.coin.coin_id] = noti.final_value
    js_data = json.dumps(dic)
    return [js_data,len(dic)]


class ChangeCurrencyFav(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            favorite_currency = request.data.get("favorite_currency")
            user = Profile.objects.get(user__id=request.user.id)
            user.fav_currency = favorite_currency
            user.save()
            return Response("Favorite currency updated")


class AllCoinInformation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        if request.method == 'GET':

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get('currency') is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get('currency')

            values = list(cryptoObject.objects
                          .annotate(current=F("value__current"),
                                    high_1d=F("value__high_1d"),
                                    low_1d=F("value__low_1d"),
                                    currency=F("value__currency"),
                                    ath=F("value__ath"),
                                    ath_time=F("value__ath_time"),
                                    atl=F("value__atl"),
                                    atl_time=F("value__atl_time"))
                          .values("coin_id",
                                  "symbol",
                                  "name",
                                  "image",
                                  "last_updated",
                                  "current",
                                  "high_1d",
                                  "low_1d",
                                  "ath",
                                  "ath_time",
                                  "atl",
                                  "atl_time")
                          .filter(Q(currency=currency))
                          .filter(coin_id=kwargs.get('id')))

            return JsonResponse(values, safe=False)

