from django.shortcuts import render,redirect

from faceapp.models import UserModel, TransactionModel
from django.contrib import messages
from django.db.models import Q
from faceapp.email import registration_mail, transaction_table
from datetime import datetime

from faceapp.decorators import user_login_required
from xhtml2pdf import pisa
from FaceDetection import settings
import os
from django.http import HttpResponse, Http404
from faceapp import face_detction
from .face_detction import *
import random



def user_login(request):
    if request.method=="POST":
        try:
            email=request.POST['email']
            password=request.POST['password']
            uqs=UserModel.objects.get(email=email,password=password)
            if uqs:
                request.session['user_id'] = uqs.id
                request.session['user_name'] = uqs.name
                return redirect("index")
        except Exception as ex:
            messages.error(request,"Invalid Email or Password")
            print(str(ex))
    return render(request, "user-login.html")


def user_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        address = request.POST['address']
        res=UserModel(name=name, email=email, mobile=mobile, password=password, address=address)
        res.save()
        status = registration_mail(name=res.name, no=res.id, username=email, password=password, to=email)
        if status == 1:
            messages.success(request, 'Email sent successfully')
        else:
            messages.error(request, 'Something went wrong. Failed to send email.')
        messages.success(request, "Registration Done Successfully")
        return redirect('user_login')
    return render(request, "user-registration.html")


def user_logout(request):
    try:
        # Flush session data
        del request.session['user_id']
        del request.session['user_name']
        request.session.flush()
    except Exception as ex:
        print("User Logout Error : ",ex)
    return redirect("user_login")

def transfer_money(request, uid, accno, amount):
    userqs = UserModel.objects.get(id=uid)
    if userqs.balance > amount:
        try:
            accto = UserModel.objects.get(id=accno)
            print(userqs,accto)
            UserModel.objects.filter(id=accno).update(balance=accto.balance + amount)  # add amount
            UserModel.objects.filter(id=uid).update(balance=userqs.balance - amount)  # deduct amount
            TransactionModel(trans_from=userqs,trans_to=accto,amount=amount).save()
            messages.success(request, "Payment done successfully.")
        except Exception as ex:
            messages.error(request, "Invalid account number.  -" + str(ex))
    else:
        messages.error(request, "Insufficient balance.")

def fetch_transaction_details(uid):
    deposit=TransactionModel.objects.filter(trans_from=uid)
    debit=TransactionModel.objects.filter(trans_to=uid)
    print("recieve from =",deposit,"transfer to",debit)
    return deposit, debit


def index(request):
    uid = request.session['user_id']
    deposit , debit = fetch_transaction_details(uid)
    print("2recieve from =",deposit,"2transfer to",debit)

    if request.method=='POST':
        request.session['accno']=request.POST.get('accno')
        request.session['amount']=request.POST['amount']
        face_detction.OTP=random.randint(1000,9999)
        print("Online message Password is ",face_detction.OTP,"%"*7)
        face_detction.detect_face(face_detction.OTP)
        return render(request, "otp.html")

    return render(request, "user-home.html", {"debit":debit,"deposit":deposit})

def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, request.session['fpath'])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_report(request):
    uid=request.session['user_id']
    uqs=UserModel.objects.get(id=uid)
    deposit, debit = fetch_transaction_details(uid)
    html_content=transaction_table(uqs=uqs,debit=debit,deposit=deposit)
    file_name=str(uid)+".pdf"
    request.session['fpath']=os.path.join(settings.MEDIA_ROOT,file_name)
    result_file = open(request.session['fpath'], "w+b")
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    result_file.close()
    if not pisa_status.err:
        messages.success(request, "PDF generated")
        download_file(request)
    else:
        messages.error(request, "Failed to generate PDF")
    return redirect("index")

def otp(request):
    print(123)
    if request.method=="POST":
        otp=request.POST["otp"]
        if otp==str(face_detction.OTP):
            if face_detction.FLAG==1:
                transfer_money(request, request.session['user_id'], request.session['accno'],int(request.session['amount']))
            else:
                download_file(request)
    return render(request,"otp.html")