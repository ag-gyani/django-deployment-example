from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')
@login_required
def special(request):
    return HttpResponse("YOU ARE LOGGED IN,NICE!  ")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered=False
    print("1")
    if request.method == "POST":
        print("2")
        user_form=UserForm(data=request.POST)
        print("3")
        profile_form=UserProfileInfoForm(data=request.POST)
        print("4")
        if user_form.is_valid() and profile_form.is_valid():
            print("5")
            user=user_form.save()
            print(user)
            print("6")
            user.set_password(user.password)
            print("7")
            user.save()
            print("8")
            profile=profile_form.save(commit=False)
            print("9")
            profile.user=user
            print("10")
            if 'profile_pic' in request.FILES:
                print("11")
                profile.profile_pic=request.FILES['profile_pic']
                print("12")
                print("mala chabuk")
            profile.save()
            print("13")
            registered=True
            print("14")

        else:
            print(user_form.errors,profile_form.errors)
            print("15")
    else:
        print("16")
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
        print("17")
    print("18")
    return render(request,'basic_app/registartion.html',
                                    {'user_form':user_form,
                                        'profile_form':profile_form,
                                        'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone trie to login and failed") 
            print("username: {} and password {}".format(username,password))
            return HttpResponse("INVALID LOGIN DETAILD SUPLIED!")
    else:
        return render(request,'basic_app/login.html',{})