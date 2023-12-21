from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from shop.models import Product
from cart.models import Cart,Order,Account

def cartview(request):
    u=request.user                       #user object
    try:
        cart=Cart.objects.filter(user=u)#user foreign key and a obj u can be passed to the foreign key
        sum=0
        for i in cart:
            sum=sum+i.quantity*i.product.price

    except:
        pass

    return render(request,'cart.html',{'c':cart,'total':sum})

@login_required
def add_to_cart(request,p):
    p=Product.objects.get(name=p)
    u=request.user          #user is a object of User table
    try:
        cart=Cart.objects.get(product=p,user=u)      #if there is a  cart obj with product p and user u
        if(cart.quantity<cart.product.stock):         # here cart.product product is the foreignkey
            cart.quantity+=1                                #then add the qty 1 of that cart obj
        cart.save()
    except:
        cart = Cart.objects.create(product=p, user=u, quantity=1)    #if no cart obj create a cart obj with pro p and user u
        cart.save()

    return redirect('cart:cartview')

def del_from_cart(request,p):
    p=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=p,user=u)
        if(cart.quantity>1):

            cart.quantity-=1
            cart.save()
        else:
            cart.delete()
    except:
             pass

    return redirect('cart:cartview')

def delete_cart(request,p):
    p=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=p,user=u)
        cart.delete()
    except:
        pass
    return redirect('cart:cartview')



def orderform(request):
    if request.method=="POST":
        a=request.POST['a']  #address
        p=request.POST['p']   #phone number
        n=request.POST['n']    #account number
        u=request.user
        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total=total+i.quantity*i.product.price

        ac=Account.objects.get(acctnum=n)   #single record from Account table

        if ac.amount>=total:
            ac.amount-=total
            ac.save()
            for i in cart:
                o=Order.objects.create(user=u,product=i.product,address=a,noofitems=i.quantity,phone=p,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()
            msg="order placed successfully"
            return render(request,'orderdetail.html',{'m':msg})

        else:
            msg="insufficient Fund"
            return render(request, 'orderdetail.html', {'m': msg})

    return render(request,'orderform.html')

def orderview(request):
    u=request.user
    try:
        o=Order.objects.filter(user=u)
    except:
        pass
    return render(request,'orderview.html',{'order':o,'user':u})