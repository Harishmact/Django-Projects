from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required



def search(request):
    q=""
    product=None
    if(request.method=="POST"):
        q=request.POST['q']        # q is the search obj
        if q:
            product=Product.objects.filter(Q(name__icontains=q)|Q(desc__icontains=q))

    return render(request,'search.html',{'p':product,'query':q})
