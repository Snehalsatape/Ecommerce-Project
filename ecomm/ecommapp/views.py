from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Product,Cart,Order
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    products = Product.objects.all()
    context={}
    context['products']=products
    print(context['products'])
    # context['name']="oreo"
    # context['age'] = 12
    return render(request,"index.html",context)


def productdetail(request,pid):
    context={}
    product = Product.objects.get(id=pid)
    context['product'] = product
    return render(request,"product_detail.html",context)

def catfilter(request,cid):
    context={}
    q1 = Q(is_active=True)
    q2 = Q(category=cid)
    products = Product.objects.filter(q1&q2)
    context['products'] = products
    return render(request,"index.html",context)


def sortbyprice(request,s):
    context={}
    if s=="0":
        products = Product.objects.all().order_by('-price')
    elif s=='1':
        products = Product.objects.all().order_by('price')
    context['products']=products
    return render(request,"index.html",context)


def pricerange(request):
    context={}
    if request.method=="GET":
        return render(request,"index.html")
    else:
        min = request.POST['min']
        max = request.POST['max']
        products = Product.objects.filter(price__gte=min,price__lte=max)
        context['products']=products
        return render(request,"index.html",context)



#user accounts
def user_registration(request):
    context={}
    if(request.method=="GET"):
        return render(request, "registration.html")
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if(uname=="" or upass=="" or ucpass==""):
            context['error']="please fill all the fields"
        elif(upass!=ucpass):
            context['error']="Password and Confirm Passwoed must be same"
        else:
            user_obj = User.objects.create(password=upass,username=uname,email=uname)
            user_obj.set_password(upass)
            user_obj.save()
            context['success']="User Registered Successfully"
        return render(request,"registration.html",context)
    

def user_login(request):
    context={}
    if (request.method=="GET"):
        return render(request,"login.html")
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        if uname=="" or upass=="":
            context['error']="please fill all the fields"
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect("/")
            else:
                context['error']="Invalid credentials"
        return render(request,"login.html",context)
    

def user_logout(request):
    logout(request)
    return redirect("/")



def addtocart(request,pid):
    if request.user.is_authenticated:
        uid = request.user.id
        u = User.objects.get(id=uid)
        p = Product.objects.get(id=pid)
        c = Cart.objects.create(uid=u,pid=p)
        c.save()
        return redirect("/")
    else:
        return redirect("/login")


def viewcart(request):
    context={}
    user_id = request.user.id
    c = Cart.objects.filter(uid = user_id)
    np = len(c)
    context['np']=np
    context['products']=c
    sum = 0
    for i in c:
        sum = sum + i.pid.price*i.quantity
        context['sum']=sum
    return render(request,"cart.html",context)


def removefromcart(request,cid):
    c =Cart.objects.get(id=cid)
    c.delete()
    return redirect("/viewcart")


def updateqty(request,cid,qv):
    c = Cart.objects.filter(id=cid)
    if qv=="1":
        t=c[0].quantity+1
        c.update(quantity=t)
    elif qv=="0":
        if c[0].quantity>1:
            t= c[0].quantity-1
            c.update(quantity=t)
        elif c[0].quantity==1:
            c.delete()
    return redirect("/viewcart")

def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        c = Cart.objects.filter(uid = user)
        order_id =random.randrange(1000,9999)
        for i in c:
            o = Order.objects.create(order_id=order_id,uid=user,pid=i.pid,quantity=i.quantity)
            o.save()
            i.delete()
        o = Order.objects.filter(uid=user)
        np = len(o)
        context={}
        context['products']=o
        context['np']=np
        sum = 0
        for i in o:
            sum = sum+i.pid.price*i.quantity
        return render(request,"order.html",context)
    else:
        return render(request,"login.html")

def makepayment(request):
    context={}
    o = Order.objects.filter(uid = request.user.id)
    sum = 0
    for i in o:
            sum = sum+i.pid.price*i.quantity
            oid=i.order_id
    context['sum']=sum*100
    client = razorpay.Client(auth=("rzp_test_FrZIWc26GigwDF", "T9zhlkBI4zTLVcADqN3GfCtz"))
    data = { "amount": 500, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    return render(request, "pay.html")

def senduseremail(request):
    send_mail(
    "Ekart Order",
    "Order placed successfully",
    "snehalsatape@gmail.com",
    ["snehalsatape@gmail.com"],
    fail_silently=False,
)
    return HttpResponse("Gmail")


#uvmp vcdw cgem uncs





