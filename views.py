from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from .models import Product,ProductImages,User,Payment
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password,check_password
from instamojo_wrapper import Instamojo
from firstproject.settings import PAYMENT_API_KEY,PAYMENT_API_AUTH_TOKEN
from django.contrib.auth.decorators import login_required
from django.db.models import Q
api = Instamojo(api_key=PAYMENT_API_KEY, auth_token=PAYMENT_API_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Create your views here.
def homepage(request):
    product=Product.objects.filter(active=True)
    return render(request,'Download/home.html',{'product':product})

def loginpage(request):
    if request.method=="POST":
        email=request.POST['email'];
        password=request.POST['password']
        try:
            user=User.objects.get(email=email)
            if user:
                if check_password(password=password,encoded=user.password):
                    dict={}
                    dict['email']=user.email;
                    dict['id']=user.id
                    dict['phone']=user.phone
                    request.session['user']=dict
                    request.session['email']=user.email
                    request.session['id']=user.id
                    return HttpResponseRedirect('/Download/home/')
                else:
                    msg="Invalid Email or Password"
                    return render(request,'Download/login.html',{'msg':msg})
        except:
            msg="Invalid Email or Password"
            return render(request,'Download/login.html',{'msg':msg})
    return render(request,'Download/login.html')

def showpage(request):
    if request.method=="GET":
        id=request.GET['id']
        print(id)
        product=Product.objects.get(id=id)
        images=ProductImages.objects.filter(product=product)
        can_download=False
        try:
            session_user=request.session.get('user')
            if session_user:
                user_id=session_user.get('id')
                user=User.objects.get(id=user_id)
                payment=Payment.objects.filter(~Q(status="Failed"),product=product,user=user)
                if len(payment)!=0:
                    if(product.file):
                        can_download=True
        except:
            pass;
        return render(request,'Download/singleproduct.html',{'product':product,'Images':images,'can_download':can_download})

def signuppage(request):
    return render(request,'Download/signup.html')


def emailverifypage(request):
    if request.method=="GET":
        email=request.GET['email']
        OTP=request.GET['OTP']
        name=request.GET['name']
        recipient=request.GET['email']
        print(OTP)
        str2='Hello Mr '+name;
        str1="Your Verification Code is "+str(OTP)
        send_mail(str2,str1,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
        return HttpResponse('true')


def page_afterverification(request):
    if request.method=="GET":
        try:
            name=request.GET['name']
            email=request.GET['email']
            password=request.GET['password']
            phone=request.GET['phone']
            user=User(name=name,email=email,phone=phone,password=make_password(password))
            user.save()
            return HttpResponse('true')
        except:
            return HttpResponse('false')

def logout(request):
    request.session.clear();
    return HttpResponseRedirect('/Download/login')


def freedownloadpage(request):
    id=request.GET['id']
    try:
        product=Product.objects.get(id=id)
        if product.discount==100:
            file=product.file
            if file:
                return redirect(product.file.url)
            else:
                return redirect(product.link)
        else:
            return HttpResponseRedirect('/Download/home/')
    except:
        return HttpResponseRedirect('/Download/home/')

import math

def downloadrequestpage(request):
    if request.method=="GET":
        id=request.GET.get('id')
        user=request.session.get('user')
        product=Product.objects.get(id=id)
        request.session['product_name']=product.name
        userObject=User.objects.get(id=request.session['id'])
        amount=product.price-((product.price)*(product.discount)/100)
        api = Instamojo(api_key=PAYMENT_API_KEY, auth_token=PAYMENT_API_AUTH_TOKEN);
        response = api.payment_request_create(
            amount=math.floor(amount),
            purpose=f'Payment For {product.name}',
            send_email=True,
            email=request.session.get('email'),
            redirect_url="http://localhost:8000/Download/complete-payment"
            )
        payment_request_id=response['payment_request']['id']
        payment=Payment(product=product,user=userObject,payment_request_id=payment_request_id)
        payment.save()
        url=response['payment_request']['longurl']
        print(response)
        return redirect(url)


def completepaymentpage(request):
    payment_id=request.GET['payment_id']
    payment_request_id=request.GET['payment_request_id']
    response = api.payment_request_payment_status(payment_request_id,payment_id)
    status=response['payment_request']['payment']['status']
    if status is not "Failed":
        payment=Payment.objects.get(payment_request_id=payment_request_id)
        payment.payment_id=response['payment_request']['payment']['payment_id']
        payment.status=status
        payment.save()
        return render(request,'Download/download_product_after_payment.html',{'product_name':product_name,'payment':payment})
    else:
        return render(request,'Download/payment_fail.html')
    print(response)
    print(payment_request_id)


def downloadAfterpayment(request):
    product=Product.objects.get(id=request.GET['id'])
    session_user=request.session.get('user')
    user=User.objects.get(id=request.session['id'])
    payment=Payment.objects.filter(user=user,product=product)
    if(len(payment)>0):
        print(len(payment))
        file=product.file
        if file:
            return redirect(product.file.url)
        else:
            return redirect(product.link)
    else:
        return redirect('/Download/home')

def OrderPage(request):
    payments=Payment.objects.filter(~Q(status="Failed"),user=request.session.get('id'))
    return render(request,'Download/orderpage.html',{'orders':payments})

import random
form="ashraf"
def forgotpasswordpage(request):
    if request.method=="GET":
        return render(request,'Download/resetpassword.html',{'form':form})
    if request.method=="POST":
        try:
            email=request.POST['email']
            user=User.objects.get(email=email);
            recipient=email
            request.session['email_passwordreset']=email
            str2="Dear User";
            OTP=math.floor(random.randint(100000,1000000));
            str1="Password Reset Verification Code is "+str(OTP)
            send_mail(str2,str1,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
            request.session['OTP-VERIFICATION-CODE']=OTP
            msg1="Verification Code Has Been Sent To Your Email.."
            return render(request,'Download/resetpassword.html',{'msg1':msg1,'email':email})
        except:
            msg="Email Id is not Valid"
            return render(request,'Download/resetpassword.html',{'msg':msg,'form':form})


def VerifyEmailForResetPassword(request):
    if request.method=="POST":
        code=int(request.POST['verify-code'])
        verify_code=request.session['OTP-VERIFICATION-CODE']
        print(type(code))
        print(type(verify_code))
        if code==verify_code:
            msg3="Email Verified"
            return render(request,'Download/resetpassword.html',{'msg3':msg3})
        else:
            msg4="Verification Code is Wrong"
            return render(request,'Download/resetpassword.html',{'msg4':msg4})

def ChangePassword(request):
    error=""
    page="ashraf"
    if request.method=="POST":
        password=request.POST['password']
        repassword=request.POST['repassword']
        if(len(password)<6):
            error="Password must be more than 6 char Long"
        elif(len(repassword)<6):
            error="Password must be more than 6 char Long"
        elif(password!=repassword):
            error="Password Not Matched"
        if error:
            return render(request,'Download/resetpassword1.html',{'error':error,'page':page})
        else:
            email=request.session['email_passwordreset']
            user=User.objects.get(email=email)
            user.password=make_password(password)
            user.save()
            msg="Your Password has been changed..."
            sendEmailAfterChangePassword(user)
            return render(request,'Download/resetpassword1.html',{'msg':msg,'page':page})

def sendEmailAfterChangePassword(user):
    str2="Dear "+user.name
    str1="Your Password Has Been Changed Successfully.."
    recipient=user.email
    send_mail(str2,str1,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
