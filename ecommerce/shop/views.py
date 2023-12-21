from django.shortcuts import render
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

def allcategories(request):
    b=Category.objects.all()
    return render(request,'category.html',{'cat':b})

def allproducts(request,p):
    c=Category.objects.get(name=p)  #creates a object (single record)
    p=Product.objects.filter(category=c)    #creates a sequence ,c is a object thus filter fun
    return render(request,'product.html',{'c':c,'p':p})



def detail(request,p):
    p=Product.objects.get(name=p)   #gets a particular product details with name=p
    return render(request,'detail.html',{'p':p})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        c=request.POST['q']
        e=request.POST['e']

        if p==c:
            u=User.objects.create_user(username=u,password=p,email=e)
            u.save()
            return render(request,'login.html')
        else:
            return HttpResponse("Password not matching")

    return render(request,'register.html')

def user_login(request):
    if request.method=="POST":
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return allcategories(request)
        else:
            messages.error(request,"Invalid credentials")
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return user_login(request)

