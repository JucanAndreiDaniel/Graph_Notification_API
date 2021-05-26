from os import name
from django.db.models.aggregates import Avg
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
import traceback
from statistics import mean

# Rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    cryptoObject,
    Profile,
    market_chart,
    value,
    Notification,
    CompanyProfile,
    StockPrices,
)

from django.db.models import F, Q


# Serializare Obiect Crypto in json
class JsonObjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == "GET":

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get("currency") is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get("currency")

            values = list(
                cryptoObject.objects.annotate(
                    current=F("value__current"),
                    high_1d=F("value__high_1d"),
                    low_1d=F("value__low_1d"),
                    currency=F("value__currency"),
                    ath=F("value__ath"),
                    ath_time=F("value__ath_time"),
                    atl=F("value__atl"),
                    atl_time=F("value__atl_time"),
                )
                .values(
                    "coin_id",
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
                    "atl_time",
                )
                .filter(Q(currency=currency))
            )

            return JsonResponse(values, safe=False)


# Serializare Favorite in functie de user


class JsonFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == "GET":

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get("currency") is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get("currency")

            favorites = list(
                user.favorite.annotate(
                    current=F("value__current"),
                    high_1d=F("value__high_1d"),
                    low_1d=F("value__low_1d"),
                    currency=F("value__currency"),
                    ath=F("value__ath"),
                    ath_time=F("value__ath_time"),
                    atl=F("value__atl"),
                    atl_time=F("value__atl_time"),
                )
                .values(
                    "coin_id",
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
                    "atl_time",
                )
                .filter(Q(currency=currency))
            )

            return JsonResponse(favorites, safe=False)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Inactive user.")
        else:
            messages.info(request, "Invalid username or password.")
            return HttpResponseRedirect("login")
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user_name = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, f"Username Taken: {user_name}")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=user_name,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.is_active = False
                user.save()
                send_email(user)
                messages.success(request, f"Account was created for {user.username}")
                return redirect("login")

        else:
            messages.info(request, "password not matching..")
            return redirect("register")

    else:
        return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


def averagePerDay(currency):
    dic={}
    cryptoPrices = market_chart.objects.all().filter(currency=currency)
    try:
        for i in range(0,len(cryptoPrices),7):
            list_avg=[]
            list_avg.append(cryptoPrices[i].media)
            list_avg.append(cryptoPrices[i+1].media)
            list_avg.append(cryptoPrices[i+2].media)
            list_avg.append(cryptoPrices[i+3].media)
            list_avg.append(cryptoPrices[i+4].media)
            list_avg.append(cryptoPrices[i+5].media)
            list_avg.append(cryptoPrices[i+6].media)
            dic[cryptoPrices[i].coin_id] = list_avg
    except:
        traceback.print_exc()
    dic = json.dumps(dic)
    return dic


@login_required(login_url="login")
def home(request):
    # base(request)
    createProfileFromUserID(request.user.id)
    user = Profile.objects.get(user__id=request.user.id)
    lista = checkPrices(request)
    dic = lista[0]
    cList = ["usd", "eur", "rub", "gbp"]
    currency = Profile.objects.get(user__id=request.user.id)
    currency = currency.fav_currency
    prices = (
        cryptoObject.objects.annotate(
            current=F("value__current"),
            high_1d=F("value__high_1d"),
            low_1d=F("value__low_1d"),
            currency=F("value__currency"),
            last_price=F("value__last_price"),
            ath=F("value__ath"),
            ath_time=F("value__ath_time"),
            atl=F("value__atl"),
            atl_time=F("value__atl_time"),
        )
        .values(
            "coin_id",
            "symbol",
            "name",
            "image",
            "last_updated",
            "current",
            "high_1d",
            "low_1d",
            "last_price",
            "ath",
            "ath_time",
            "atl",
            "atl_time",
        )
        .filter(Q(currency=currency))
    )
    dic1 = {}
    page = request.GET.get("page", 1)
    favorites = (
        user.favorite.annotate(
            current=F("value__current"),
            high_1d=F("value__high_1d"),
            low_1d=F("value__low_1d"),
            currency=F("value__currency"),
            last_price=F("value__last_price"),
            ath=F("value__ath"),
            ath_time=F("value__ath_time"),
            atl=F("value__atl"),
            atl_time=F("value__atl_time"),
        )
        .values(
            "coin_id",
            "symbol",
            "name",
            "image",
            "last_updated",
            "current",
            "high_1d",
            "low_1d",
            "last_price",
            "ath",
            "ath_time",
            "atl",
            "atl_time",
        )
        .filter(Q(currency=currency))
    )
    cList.remove(user.fav_currency)

    pret_zi = market_chart.objects.annotate(
        last_price=F("coin__value__last_price")
    ).values("coin_id",
            "price1",
            "price2",
            "price3",
            "price4",
            "price5",
            "price6",
            "price7",
            "price8",
            "price9",
            "price10",
            "price11",
            "price12",
            "price13",
            "price14",
            "price15",
            "price16",
            "price17",
            "price18",
            "price19",
            "price20",
            "price21",
            "price22",
            "price23",
            "price24",
            "last_price").filter(day=market_chart.Days.ONE).filter(currency=currency)
    for j in pret_zi:
        dic1[f"{j['coin_id']}"] = [
            [j["last_price"]],
            [j["price1"],
            j["price2"],
            j["price3"],
            j["price4"],
            j["price5"],
            j["price6"],
            j["price7"],
            j["price8"],
            j["price9"],
            j["price10"],
            j["price11"],
            j["price12"],
            j["price13"],
            j["price14"],
            j["price15"],
            j["price16"],
            j["price17"],
            j["price18"],
            j["price19"],
            j["price20"],
            j["price21"],
            j["price22"],
            j["price23"],
            j["price24"]]
        ]
    paginator = Paginator(prices, 30)
    charts = json.dumps(dic1)
    avg_day = averagePerDay(currency)
    try:
        price = paginator.page(page)
    except PageNotAnInteger:
        price = paginator.page(1)
    except EmptyPage:
        price = paginator.page(paginator.num_pages)
    return render(
        request,
        "home.html",
        {
            "crypto": price,
            "fav": favorites,
            "notificare": dic,
            "nrnot": lista[1],
            "currencyList": cList,
            "favC": user.fav_currency,
            "chart": charts,
            "avgDay": avg_day,
        },
    )


def averagePricePerDay(mchart):
    print(mchart)
    return


def stock(request):
    stock_data = CompanyProfile.objects.annotate(
        closed=F("stockprices__closed"),
        high24=F("stockprices__high24"),
        low24=F("stockprices__low24"),
        open=F("stockprices__open"),
        previous_closed=F("stockprices__previous_closed"),
    ).values(
        "country",
        "exchange",
        "date_founded",
        "market_cap",
        "company_name",
        "shareOutstanding",
        "symbol",
        "weburl",
        "logo",
        "finnhubIndustry",
        "closed",
        "high24",
        "low24",
        "open",
        "previous_closed",
    )
    page = request.GET.get("page", 1)
    paginator = Paginator(stock_data, 30)
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    return render(request, "stock.html", {"stonks": stocks})


def filter(request):
    lista = checkPrices(request)
    dic = lista[0]
    user = Profile.objects.get(user__id=request.user.id)
    currency = Profile.objects.get(user__id=request.user.id)
    currency = currency.fav_currency
    cList = ["usd", "eur", "rub", "gbp"]
    contain = request.GET.get("contain")
    if contain == "":
        return home(request)
    prices = (
        cryptoObject.objects.annotate(
            current=F("value__current"),
            high_1d=F("value__high_1d"),
            low_1d=F("value__low_1d"),
            currency=F("value__currency"),
        )
        .filter(Q(currency=currency))
        .filter(coin_id__contains=contain)
    )
    page = request.GET.get("page", 1)
    favorites = value.objects.filter(currency=currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id)
    )
    paginator = Paginator(prices, 10)
    try:
        price = paginator.page(page)
    except PageNotAnInteger:
        price = paginator.page(1)
    except EmptyPage:
        price = paginator.page(paginator.num_pages)
    return render(
        request,
        "home.html",
        {
            "crypto": price,
            "fav": favorites,
            "notificare": dic,
            "nrnot": lista[1],
            "currencyList": cList,
            "favC": user.fav_currency,
        },
    )


def base(request):
    webpush_settings = getattr(settings, "WEBPUSH_SETTINGS", {})
    vapid_key = webpush_settings.get("VAPID_PUBLIC_KEY")
    user = request.user
    dic = checkPrices(request)
    return render(
        request, "base.html", {user: user, "vapid_key": vapid_key, "notificare": dic}
    )


def createProfileFromUserID(id):
    try:
        profile = Profile.objects.create(user_id=id)
    except:
        pass


def addToFav(user, crypto_id):
    profile = Profile(user=user)
    crypto_add = cryptoObject.objects.get(coin_id=crypto_id)
    profile.save()
    profile.favorite.add(crypto_add)
    profile.save()
    return


def addToFavorite(request):
    if request.method == "POST":
        # request form html the name of crypto to be added to favorites
        add_favorite = request.POST["crypto.id"]
        # the name of user who requested a favorite crypto
        user = User.objects.filter(username=request.user.username).get()
        addToFav(user, add_favorite)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


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
    crypto_delete = cryptoObject.objects.filter(coin_id=crypto_id).get()
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
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteFromFavApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == "POST":
            delete_favorite = request.data.get("crypto_id")
            print(delete_favorite)
            user = User.objects.filter(username=request.user.username).get()
            deleteFav(user, delete_favorite)
            return Response("Deleted")


def changeFavCurrency(request):
    user = Profile.objects.get(user__id=request.user.id)
    if request.method == "POST":
        favoriteCurrency = request.POST["curr"]
        user.fav_currency = favoriteCurrency
        user.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return Response("something went wrong")


@login_required(login_url="login")
def notificationTab(request):

    lista = checkPrices(request)
    dic = lista[0]
    currency = Profile.objects.get(user__id=request.user.id)
    currency = currency.fav_currency
    user = Profile.objects.get(user__id=request.user.id)
    favorites = (
        user.favorite.annotate(
            current=F("value__current"),
            high_1d=F("value__high_1d"),
            low_1d=F("value__low_1d"),
            currency=F("value__currency"),
            ath=F("value__ath"),
            ath_time=F("value__ath_time"),
            atl=F("value__atl"),
            atl_time=F("value__atl_time"),
        )
        .values(
            "coin_id",
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
            "atl_time",
        )
        .filter(Q(currency=currency))
    )

    notification_coins = (
        Profile.objects.get(user__id=request.user.id)
        .notification.annotate(
            current=F("coin__value__current"),
            high_1d=F("coin__value__high_1d"),
            low_1d=F("coin__value__low_1d"),
            currency=F("coin__value__currency"),
            ath=F("coin__value__ath"),
            ath_time=F("coin__value__ath_time"),
            atl=F("coin__value__atl"),
            atl_time=F("coin__value__atl_time"),
            image=F("coin__image"),
            name=F("coin__name"),
        )
        .values(
            "coin_id",
            "coin",
            "value_type",
            "initial_value",
            "final_value",
            "enabled",
            "via_mail",
            "current",
            "high_1d",
            "low_1d",
            "ath",
            "ath_time",
            "atl",
            "atl_time",
            "image",
            "name",
        )
        .filter(Q(currency=currency))
    )
    return render(
        request,
        "notificationTab.html",
        {
            "favorites": favorites,
            "notificari": notification_coins,
            "notificare": dic,
            "nrnot": lista[1],
        },
    )


def modifyNotification(request):
    if request.method == "POST":
        noti_disable = Profile.objects.get(user__id=request.user.id).notification.get(
            coin_id=request.POST.get("crypto_id")
        )
        noti_disable.enabled = bool(request.POST.get("state"))
        noti_disable.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class changeEnabledNoti(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        noti_disable = Profile.objects.get(user__id=request.user.id).notification.get(
            coin_id=request.POST.get("crypto_id")
        )
        if request.POST.get("state") == "true":
            noti_disable.enabled = True
        else:
            noti_disable.enabled = False
        noti_disable.save()
        return Response(f"Notification State:{noti_disable.enabled}")


def createNotification(request):
    if request.method == "POST":
        user = Profile.objects.get(user__id=request.user.id)
        coin_result = cryptoObject.objects.get(
            coin_id=request.POST.get("optionCrypto").lower()
        )
        option = request.POST.get("option")
        crypto_value = (
            cryptoObject.objects.annotate(
                current=F("value__current"), currency=F("value__currency")
            )
            .values("current", "currency")
            .filter(Q(currency=user.fav_currency))
            .get(coin_id=request.POST.get("optionCrypto").lower())
        )
        crypto_value = crypto_value["current"]
        final_value = float(request.POST.get("value"))

        if final_value < 0:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if option == "g_perc" or option.startswith("Growth"):
            option = "g_perc"
            final_value = crypto_value + (crypto_value * final_value) / 100
        elif option == "d_perc" or option.startswith("Decrease"):
            option = "d_perc"
            if final_value >= 100:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            final_value = crypto_value - (crypto_value * final_value) / 100
        else:
            option_list = option.split()
            if option_list[0] == "Value":
                option = option_list[1].lower()

        if request.POST.get("viamail") == "on":
            viamail = True
        else:
            viamail = False
        try:
            notificare = user.notification.get(
                coin_id=request.POST.get("optionCrypto").lower()
            )
            notificare.value_type = option
            notificare.final_value = final_value
            notificare.via_mail = viamail

        except:
            notificare = Notification(
                coin=coin_result,
                value_type=option,
                initial_value=crypto_value,
                final_value=final_value,
                via_mail=viamail,
            )

        notificare.save()
        user.notification.add(notificare)
        user.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class CreateNotificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == "POST":
            user = Profile.objects.get(user__id=request.user.id)
            coin_result = cryptoObject.objects.get(
                coin_id=request.POST.get("crypto_id")
            )
            option = request.POST.get("option")
            crypto_value = (
                cryptoObject.objects.annotate(
                    current=F("value__current"), currency=F("value__currency")
                )
                .values("current", "currency")
                .filter(Q(currency=user.fav_currency))
                .get(coin_id=request.POST.get("crypto_id").lower())
            )
            crypto_value = crypto_value["current"]
            final_value = float(request.POST.get("value"))

            if final_value < 0:
                return Response(data="Incorrect Values", status=400)
            if option == "g_perc" or option.startswith("Growth"):
                option = "g_perc"
                final_value = crypto_value + (crypto_value * final_value) / 100
            elif option == "d_perc" or option.startswith("Decrease"):
                option = "d_perc"
                if final_value >= 100:
                    return Response(data="Incorrect Values", status=400)
                final_value = crypto_value - (crypto_value * final_value) / 100
            else:
                option_list = option.split()
                if option_list[0] == "Value":
                    option = option_list[1].lower()

            if request.POST.get("viamail") == "true":
                viamail = True
            else:
                viamail = False
            try:
                notificare = user.notification.get(
                    coin_id=request.POST.get("crypto_id")
                )
                notificare.value_type = option
                notificare.final_value = final_value
                notificare.via_mail = viamail

            except:
                notificare = Notification(
                    coin=coin_result,
                    value_type=option,
                    initial_value=crypto_value,
                    final_value=final_value,
                    via_mail=viamail,
                )

            notificare.save()
            user.notification.add(notificare)
            user.save()
            return Response("Notification Created")


def deleteNotification(request):
    noti_delete = Profile.objects.get(user__id=request.user.id).notification.get(
        coin_id=request.POST.get("crypto_delete")
    )
    noti_tabela_mare = Notification.objects.get(id=noti_delete.id).delete()
    profile = Profile(user=request.user)
    profile.notification.remove(noti_delete)
    profile.save()
    print(noti_delete)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteNotificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == "POST":
            noti_delete = Profile.objects.get(
                user__id=request.user.id
            ).notification.get(coin_id=request.POST.get("crypto_id"))
            noti_tabela_mare = Notification.objects.get(id=noti_delete.id).delete()
            profile = Profile(user=request.user)
            profile.notification.remove(noti_delete)
            profile.save()
            return Response("Notication Deleted")


def changeNotification(request):
    user = Profile.objects.get(user__id=request.user.id)

    option = request.POST.get("option")
    crypto_value = (
        cryptoObject.objects.annotate(
            current=F("value__current"), currency=F("value__currency")
        )
        .values("current", "currency")
        .filter(Q(currency=user.fav_currency))
        .get(coin_id=request.POST.get("crypto_name"))
    )
    crypto_value = crypto_value["current"]
    final_value = request.POST.get("cvalue")
    if final_value == "":
        notificare = Profile.objects.get(user__id=request.user.id).notification.get(
            coin_id=request.POST.get("crypto_name")
        )
        final_value = notificare.final_value
    else:
        final_value = float(final_value)
        if final_value < 0:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if option == "g_perc":
            final_value = crypto_value + (crypto_value * final_value) / 100
        elif option == "d_perc":
            if final_value >= 100:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            final_value = crypto_value - (crypto_value * final_value) / 100
        else:
            final_value = final_value

    viamail = request.POST.get("viamail")
    if viamail == "on":
        viamail = True
        notificare = Profile.objects.get(user__id=request.user.id).notification.get(
            coin_id=request.POST.get("crypto_name")
        )

        notificare.value_type = option
        notificare.final_value = final_value
        notificare.via_mail = viamail

        notificare.save()
        user.notification.add(notificare)
        user.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    notificare = Profile.objects.get(user__id=request.user.id).notification.get(
        coin_id=request.POST.get("crypto_name")
    )
    notificare.value_type = option
    notificare.final_value = final_value
    notificare.save()
    user.notification.add(notificare)
    user.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def checkPrices(request):
    user = Profile.objects.get(user__id=request.user.id)
    notification_coins = user.notification.all()

    favorites = value.objects.filter(currency=user.fav_currency).filter(
        coin__in=cryptoObject.objects.filter(profile__user__id=request.user.id)
    )

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
    return [js_data, len(dic)]


class ChangeCurrencyFav(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == "POST":
            favorite_currency = request.data.get("favorite_currency")
            user = Profile.objects.get(user__id=request.user.id)
            user.fav_currency = favorite_currency
            user.save()
            return Response("Favorite currency updated")


class AllCoinInformation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        if request.method == "GET":

            user = Profile.objects.get(user__id=request.user.id)

            if request.GET.get("currency") is None:
                currency = user.fav_currency
            else:
                currency = request.GET.get("currency")

            values = list(
                cryptoObject.objects.annotate(
                    current=F("value__current"),
                    high_1d=F("value__high_1d"),
                    low_1d=F("value__low_1d"),
                    currency=F("value__currency"),
                    ath=F("value__ath"),
                    ath_time=F("value__ath_time"),
                    atl=F("value__atl"),
                    atl_time=F("value__atl_time"),
                )
                .values(
                    "coin_id",
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
                    "atl_time",
                )
                .filter(Q(currency=currency))
                .filter(coin_id=kwargs.get("id"))
            )

            return JsonResponse(values, safe=False)


class UserNotifications(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == "GET":

            user = Profile.objects.get(user__id=request.user.id)

            values = list(user.notification.all().values())

            return JsonResponse(values, safe=False)


def cmpProfile(contain, cee):
    a = CompanyProfile.objects.annotate(
        closed=F("stockprices__closed"),
        high24=F("stockprices__high24"),
        low24=F("stockprices__low24"),
        open=F("stockprices__open"),
        previous_closed=F("stockprices__previous_closed"),
    ).values(
        "country",
        "exchange",
        "date_founded",
        "market_cap",
        "company_name",
        "shareOutstanding",
        "symbol",
        "weburl",
        "logo",
        "finnhubIndustry",
        "closed",
        "high24",
        "low24",
        "open",
        "previous_closed",
    )
    if contain != "":
        if cee == "symbol":
            a = a.filter(symbol__icontains=contain)
        elif cee == "name":
            a = a.filter(company_name__icontains=contain)

    return a


def stockTickFinder(request):
    symbolOrName = request.GET.get("contain")
    print(symbolOrName)
    companiesSymbol = cmpProfile(symbolOrName, "symbol")
    namez = cmpProfile(symbolOrName, "name")
    if companiesSymbol:
        page = request.GET.get("page", 1)
        paginator = Paginator(companiesSymbol, 30)
        try:
            companiesSymbol = paginator.page(page)
        except PageNotAnInteger:
            companiesSymbol = paginator.page(1)
        except EmptyPage:
            companiesSymbol = paginator.page(paginator.num_pages)
        return render(request, "stock.html", {"stonks": companiesSymbol})
    if namez:
        page = request.GET.get("page", 1)
        paginator = Paginator(namez, 30)
        try:
            namez = paginator.page(page)
        except PageNotAnInteger:
            namez = paginator.page(1)
        except EmptyPage:
            namez = paginator.page(paginator.num_pages)
        return render(request, "stock.html", {"stonks": namez})
    allz = cmpProfile("", "all")
    return render(request, "stock.html", {"stonks": allz})
