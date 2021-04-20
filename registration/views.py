from typing import Tuple
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
# Rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import cryptoObject, Profile


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

# TODO Inca un endpoint


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

    prices = cryptoObject.objects.filter(currency="usd")
    page = request.GET.get('page', 1)
    favorites = cryptoObject.objects.filter(profile__user__id=request.user.id,currency="eur")
    paginator = Paginator(prices, 30)
    try:

        price = paginator.page(page)
    except PageNotAnInteger:

        price = paginator.page(1)
    except EmptyPage:

        price = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"crypto": price, "fav": favorites})

@login_required(login_url="login")
def addToFavorite(request):
    if request.method == 'POST':
        add_favorite = request.POST["crypto.id"] # request form html the name of crypto to be added to favorites
        user = User.objects.filter(username=request.user.username).first() # the name of user who requested a favorite crypto 
        crypto_add = cryptoObject.objects.filter(coin_id=add_favorite).first() # user defines what type of currency does he want to be added later :) 
        profile = Profile(user=user)
        profile.favorite.add(crypto_add)
        profile.save()
        return HttpResponseRedirect('/')
        
@login_required(login_url="login")
def deleteFromFavorite(request):
    if request.method == 'POST':
        delete_favorite = request.POST["crypto.id"] # request form html the name of crypto to be added to favorites
        user = User.objects.filter(username=request.user.username).first() # the name of user who requested a favorite crypto 
        crypto_delete = cryptoObject.objects.filter(coin_id=add_favorite).first() # user defines what type of currency does he want to be added later :) 
        profile = Profile(user=user)
        profile.favorite.remove(crypto_delete)
        profile.save()
        return HttpResponseRedirect('/')

