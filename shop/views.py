from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Contact,Order,OrderUpdate,UserDetail
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

MERCHANT_KEY = '9851kOuQlWgQ4YtV';
# Create your views here.
def awlogin(request):
    if request.method== "POST":
        username=request.POST["username1"]
        password=request.POST["password1"]
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect("ShopHome")
        else:
            messages.error(request,"Invalid Username and Password")
            return redirect("ShopHome")
    else:
        return render(request,"shop/error404.html")


@login_required(login_url='/shop/error404')
def awlogout(request):
    logout(request)
    messages.success(request,"Successfull Logged Out")
    return redirect("ShopHome")


def signup(request):
    if request.method== "POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirmpassword=request.POST["confirmpassword"]
        print(username)   
        if User.objects.filter(username=username).exists():
            messages.error(request,"This username already exist. Please choose another username")
            return redirect("ShopHome")
        else: 
            myuser=User.objects.create_user(username,email,password)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            myuserdetail=UserDetail(username=username)
            myuserdetail.save()
            msgback=f"Hi {fname} Welcome to AwesomeCart and thanks to join us"
            send_mail("Account created successfully",msgback,settings.EMAIL_HOST_USER,[email],fail_silently=False)
            messages.success(request,"You have successfully created your AwesomeCart Account")
            return redirect("ShopHome")
    else:
        return render(request,"shop/error404.html")
        
 
def index(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    allproducts=Product.objects.all()
    l=[]
    for i in allproducts:
        l.append(i.category)
    s=set(l)
    l=list(s)
    productallcategory=[]
    for i in l:
        products=[]
        for j in allproducts:
            if j.category==i:
                products.append(j)
        n=len(products)
        nSlides=n//4+ceil((n/4)-(n//4))
        rs=range(1,nSlides)
        productallcategory.append([products,nSlides,rs,i])
    d={'productallcategory':productallcategory,'img':img}
    return render(request,'shop/index.html',d)


def about(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    return render(request,'shop/about.html',{'img':img})


def contact(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    if(request.method=='POST'):
        name=request.POST["namecont"]
        print(name)
        email=request.POST["emailcont"]
        print(email)
        phone=request.POST["phonecont"]
        print(phone)
        desc=request.POST["desccont"]
        print(desc)
        cont=Contact(name=name,email=email,phone=phone,desc=desc)
        cont.save()
        messages.success(request,"You have been successfully submitted your Query")
        return redirect("ShopHome")
    return render(request,'shop/contact.html',{'img':img})


def tracker(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    if(request.method=="POST"):
        orderid=request.POST["orderidtrc"]
        print("hi"+orderid)
        email=request.POST["emailtrc"]
        obj=Order.objects.filter(order_id=orderid,email=email)          # To chk whether there is any order with this orderid or not 
        print(obj)
        if obj:
            ind=True
            obj1=OrderUpdate.objects.filter(order_id=orderid)         # To fetch the tracking status these object can be more than one
            print(obj1)
            obj2=Order.objects.get(order_id=orderid)               # To fetch the  Items with this orderid  from Order Table 
            cart=json.loads(obj2.items)
            orderid=obj2.order_id
            d={'statusobjects':obj1,'cart':cart,'img':img,'orderid':orderid,'ind':ind,'obj2':obj2}
            return render(request,'shop/tracking.html',d)
            
        else:
            messages.error(request,"Sorry there is no order with this orderid and email")
            return redirect("TrackingStatus")
    return render(request,'shop/tracking.html',{'img':img})


def search(request):
    l=[]
    print("search")
    #print(request.POST)
    print(request.GET)
    query=request.GET.get("search")
    print(query)
    print(type(query))
    objs=Product.objects.all()
    for obj in objs:
        qw=query.lower()
        a=obj.product_name.lower()
        b=obj.category.lower()
        c=obj.sub_category.lower()
        d=obj.desc.lower()
        p=a.find(qw)
        q=qw.find(b)
        r=qw.find(c)
        s=d.find(qw)
        if p==-1 and q==-1 and r==-1 and s==-1:
            pass
        else:
            l.append(obj)
    print(l)
    n=len(l)
    nSlides=n//4+ceil((n/4)-(n//4))
    rs=range(1,nSlides)
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    d={'allprod':l,'ns':nSlides,'rs':rs,'img':img,'query':query}
    if(len(l)==0):
        messages.error(request,"Oops! Sorry There is no product ")
        return redirect("Error404")
    else:
        return render(request,'shop/search.html',d)


def prodView(request,myid):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    product=Product.objects.filter(id=myid)
    d={'product':product[0],'img':img}
    print(product)
    return render(request,'shop/prodview.html',d)


def checkout(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    if(request.method=="POST"):
        items=request.POST["items"]
        amount=request.POST["amount"]
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        add=request.POST["add1"]+" "+request.POST["add2"] 
        city=request.POST["city"]
        state=request.POST["state"]
        pin=request.POST["pin"]
        order=Order(items=items,amount=amount,name=name,email=email,phone=phone,add=add,city=city,state=state,pin=pin)
        order.save()
        ids=order.order_id
        update=OrderUpdate(order_id=ids,update_desc="The order has been placed")
        update.save()
        paytm_dict={
            "MID": "LIhfZO24888719669713",
            "ORDER_ID": str(ids),
            "CUST_ID": "email",
            "TXN_AMOUNT":str(amount),
            "CHANNEL_ID": "WEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "WEBSITE": "WEBSTAGING",
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        paytm_dict['CHECKSUMHASH']=Checksum.generate_checksum(paytm_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{"paytm_dict":paytm_dict,'img':img})                    # PAYMENT PROB 1
    return render(request,'shop/checkout.html',{'img':img})

@csrf_exempt
def handlerequest(request):
    form=request.POST
    print(form)
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print("ORDER SUCCESSFUL")
            ind=1
            if request.user.is_authenticated:
                user=UserDetail.objects.get(username=request.user.username)
                img=user.userimage
                print(img)
                print("logged In")
            else:
                img=1
                print("logged Out")
        else:
            print("ORDER WAS NOT SUCCESSFUL BECAUSE"+response_dict['RESPMSG'])
            ind=0
    return render(request,'shop/paytmstatus.html',{'response':response_dict,'ind':ind})


def error404(request):
    return render(request,"shop/error404.html")


@login_required(login_url='/shop/error404')
def myprofile(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    user = User.objects.get(username=request.user.username)
    userdetail=UserDetail.objects.filter(username=user)
    for x in userdetail:
        d={'userinfo':x,'img':img}
    return render(request,"shop/myprofile.html",d)


@login_required(login_url='/shop/error404')
def editinfo(request):
    if request.user.is_authenticated:
        userdt=UserDetail.objects.get(username=request.user.username)
        img=userdt.userimage
        d={'userdt':userdt,'img':img}
        print(img)
    else:
        img=1
    if request.method=="POST":
        activeusername = User.objects.get(username=request.user.username)
        username=request.POST["editusername"]
        fname=request.POST["editfname"]
        lname=request.POST["editlname"]
        email=request.POST["editemail"]
        phone=request.POST["editphone"]
        add=request.POST["editadd1"]+" "+request.POST["editadd2"] 
        city=request.POST["editcity"]
        state=request.POST["editstate"]
        pin=request.POST["editpin"]
        UserDetail.objects.filter(username=activeusername).update(username=username,phone=phone,add=add,city=city,state=state,pin=pin)
        User.objects.filter(username=activeusername).update(username=username,first_name=fname,last_name=lname,email=email)
        messages.success(request,"Your Details has been successfully updated")
        return redirect("ShopHome")
    return render(request,"shop/editinfo.html",d)


@login_required(login_url='/shop/error404')
def uploadimage(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    if request.method=="POST":
        print(request.FILES)
        print(request.FILES["image"])
        image=request.FILES["image"]
        activeusername = User.objects.get(username=request.user.username)
        print(activeusername)
        #UserDetail.objects.filter(username=activeusername).update(userimage=image)
        obj=UserDetail.objects.get(username=activeusername)
        obj.userimage=image
        obj.save()
        messages.success(request,"Image Uploaded Successfull")
        return redirect("ShopHome")
    else:
        return render(request,"shop/error404.html",{'img':img})


def winp(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    messages.info(request,"We will update this page soon")
    return render(request,"shop/winp.html",{'img':img})


def blog(request):
    if request.user.is_authenticated:
        user=UserDetail.objects.get(username=request.user.username)
        img=user.userimage
        print(img)
    else:
        img=1
    messages.info(request,"We will update this page soon")
    return render(request,"shop/blog.html",{'img':img})
