from django.shortcuts import render , redirect , HttpResponse
from .models import Account
from django.core.mail import send_mail
from django.conf import settings

import random
# Create your views here.
def index(request):
    return render(request,"index.html")
    

def create(request):
    if request.method  == "POST":
        name = request.POST['name']
        dob = request.POST['dob']
        aadhar = request.POST['aadhar']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        print(name,dob,phone,aadhar,address)
        Account.objects.create(name = name,DOB=dob,Aadhar = aadhar,mobile = phone,address = address,email= email)
        # print("successfull")
        send_mail( f"hello {name},thank you for creating an acc in our bank", # subject
        "FBH fraud bank of hyd , \n welcome to family of our bank \n we are happy for it \n , regards \n manager(DJD-E1)\n thank you ****!"# body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False
            )
        print("sent succesfully")
    return render(request,"create.html")


def pin_gen(request):
    if request.method == "POST":
        otp = random.randint(100000,999999)
        acc = request.POST.get('acc')
        data = Account.objects.get(acc= acc)
        email = data.email
        send_mail( f"hello {data.name}",
                  
        f"FBH fraud bank of hyd , \n the OTP (One time Password ) is {otp} \n please share the otp only with our employees not for the outside scamers , it is kind request \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False
            )
        print("sent succesfully")
        data.otp = otp 
        data.save()
        return redirect("otp")
    return render(request,'pin.html')


def valid_otp(request):
    if request.method == "POST":
        acc = request.POST['acc']
        otp = int(request.POST['otp'])
        pin1 = int(request.POST['pin1'])
        pin2 = int(request.POST['pin2'])
        if pin1 == pin2:
            data = Account.objects.get(acc= acc)
            if data.otp == otp :
                data.pin = pin2
                data.save()
                send_mail( f"hello {data.name} PIN GENERATION ",
                  
                f"FBH fraud bank of hyd , \n the we are happy to scam you  \n you successfully generated pin, we are happy to inform that we know ur otp and pin as well so we are happy to use ur money `(ur money is our money & our money is our money )` \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
                ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
            )
                print("sent succesfully")
            else:
                return HttpResponse("OTP missmatched ")
        else:
            return HttpResponse("****** is not a valid pin u ******")
    return render(request,'valid_otp.html')

def balance(request):
    data = None
    msg = ""
    bal = 0
    f = False
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        try:
            data = Account.objects.get(acc = int(acc))
        except:
            pass
        if data is not None:
            if data.pin == int(pin):
                bal = data.bal
                f = True

            else:
                msg = "pls enter the valid  pin"

        else:
            msg = "pls enter the valid account number"

    context = {
        'bal':bal,
        'var' : f,
        'msg':msg
    }
    return render(request,'bal.html',context)



def withdrawl(request):
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(acc = acc)
        except:
            print("acc not found")
        if data.pin == int(pin):
            if data.bal >= amt and amt >0:
                data.bal -= amt
                data.save()
                send_mail( f"hello {data.name} WHITHDRAWL ",
                    
                    f"FBH fraud bank of hyd , \n from ur {data.acc}  \n ,{amt} as be withdrawled from ATM the availble balance is {data.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
                )
                print("sent succesfully")
                return redirect("home")
            else:
                print("no money")
            
        else:
            print("incorrect pin")

    
    return render(request,'with.html')


def deposit(request):
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(acc = acc)
        except:
            print("acc not found")
        if data.pin == int(pin):
            if amt >= 100 and amt <= 10000:
                data.bal += amt
                data.save()
                send_mail( f"hello {data.name} DEPOSIT ",
                    
                    f"FBH fraud bank of hyd , \n from ur {data.acc}  \n ,{amt} as be deposited to ur acc {data.acc}  balance is {data.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
                )
                print("sent succesfully")
                return redirect("home")
            else:
                print("no money")
            
        else:
            print("incorrect pin")

    
    return render(request,'deposit.html')

def transfer(request):
    msg = ""
    if request.method == "POST":
        f_acc = request.POST.get('f_acc')
        t_acc = request.POST.get('t_acc')
        pin = request.POST.get('pin')
        amt = request.POST.get('amt')
        try:
            from_acc = Account.objects.get(acc = f_acc)
        except:
            msg = "send accout is not valid"
        try:
            to_acc = Account.objects.get(acc = t_acc)
        except:
            msg = "reciever account is not valid"
        if from_acc.pin == int(pin):
            if int(amt)>100 and int(amt)<=10000 and int(amt) <= from_acc.bal:
                from_acc.bal-=int(amt)
                from_acc.save()
                send_mail( f"hello {from_acc.name} ACCOUNT TRANSFER ",
                    
                    f"FBH fraud bank of hyd , \n from ur {from_acc.acc}  \n ,{amt} as be debited to  {to_acc.acc} acc  balance is {from_acc.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[from_acc.email],fail_silently=False
                )
                print("sent succesfully")
                to_acc.bal += int(amt)
                to_acc.save()
                send_mail( f"hello {from_acc.name} ACCOUNT TRANSFER ",
                    
                    f"FBH fraud bank of hyd , \n  {to_acc.acc}  \n ,{amt} YOUR acc has been credited from   {from_acc.acc} acc  balance is {to_acc.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[to_acc.email],fail_silently=False
                )
                print("sent succesfully")

            else:
                msg = "enter the valid amt"


        else:
            msg = "incoorect pin"

    return render(request,'transfer.html',{'msg':msg})
