from django.shortcuts import render
from . import forms
from first_app.models import Topic, Webpage, AccessRecord
from first_app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    webpage_list = AccessRecord.objects.order_by('date')
    my_dict = {'access_record': webpage_list,
               'text': 'hello world',
               'number': 100}
    return render(request, 'first_app/index.html', context=my_dict)

def form_name_views(request):
    form = forms.FormName()

    if request.method == "POST":
        form = forms.FormName(request.POST)
        if form.is_valid():
            print("validation success")
            print("Name:"+form.cleaned_data['name'])
            print("Email:"+form.cleaned_data['email'])
            print("Text:"+form.cleaned_data['text'])
    return render(request, 'first_app/form.html', {'form': form})

def other(request):
    return render(request, 'first_app/other.html')

def related(request):
    return render(request, 'first_app/relative.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pics' in request.FILES:
                profile.profile_pic = request.FILES['profile_pics']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'first_app/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('first_app:index'))

            else:
                return HttpResponseRedirect("ACCOUNT NOT ACTIVE")
        else:
            print("account break")
            print("username: {} and password: {}".format(username, password))
            return HttpResponse("invalid login detail")
    else:
        return render(request, 'first_app/login.html')

def special(request):
    return HttpResponse("Logged success")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('first_app:index'))

