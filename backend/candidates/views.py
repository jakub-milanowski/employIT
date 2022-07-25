from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.middleware.csrf import get_token
from rest_framework import status
import json
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm

@csrf_protect
def loginUser(request):

    if request.user.is_authenticated:
        return JsonResponse({'status': request.user.username})
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

            if user is not None:
                login(request, user)
                return JsonResponse({'username': request.user.username})
            else:
                return JsonResponse({'status': 'incorrect login or password'})
        else:
            return JsonResponse({'status': 'incorrect login or password'})
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def getCsrfToken(request):
    token = get_token(request)
    response = HttpResponse(status=status.HTTP_200_OK)
    response.set_cookie(key='csrftoken', value=token)
    return response

@csrf_protect
def registerUser(request):

    if request.user.is_authenticated:
        return JsonResponse({'status': 'already logged in'})

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
            user.save()
            return HttpResponse(status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST, safe=False)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)