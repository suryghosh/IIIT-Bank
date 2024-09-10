from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Bank_branches,AccountNumber,Transaction,Customer,Account
import random
from datetime import datetime,date

# Create your views here.
generated_numbers = set()

def gen_12_digit_number():
    random_number = random.randint(100000000000,999999999999)
    if  random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def starting_page(request):
    return render(request,'myapp/startingPage.html')



# Create your views here.
def CreatePage(request):
    branches = Bank_branches.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        #to check if phone number present in database or not
        if phone_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                print(i)
                if i.phone_no == phone_no:
                    print("true")
                    error = "phone_num"
                    return render(request,'myapp/error.html',{'error':error})
                
        aadhar_no = request.POST.get('Aadhar_no')
        #to check if aadhar number present in database or not
        if aadhar_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if i.Aadhar_no == aadhar_no:
                    error = "aadhar_num"
                    return render(request,'myapp/error.html',{'error':error})
                
        DOB = request.POST.get('DOB')
        #to check age about 18
        if DOB:
            dob = datetime.strptime(DOB, '%Y-%m-%d').date()
            age = calculate_age(dob)
            if age < 18:
                error_message = 'You must be at least 18 years old to open a account.'
                return render(request, 'myapp/error.html', {'error_message': error_message})
        branch_id = request.POST.get('branch')
        password = request.POST.get('password')
        Account_number = gen_12_digit_number()
        
        branch = Bank_branches.objects.get(branch_id=branch_id)
        accountNumber = AccountNumber(account_number = Account_number)
        customer = Customer(name=name,phone_no=phone_no,Aadhar_no=aadhar_no,DOB=DOB,branch_connect = branch,password=password,account=accountNumber)
        account = Account(account_type = 'current',account_number=accountNumber)
        accountNumber.save()
        customer.save()
        account.save()
        return redirect(f'/accountNumber/{Account_number}')
    return  render(request,'myapp/CreatePage.html',{'branches':branches,})

#showing account number page
def showAccountNum(request, account_num):
    account = AccountNumber.objects.get(account_number=account_num)
    customer = Customer.objects.get(account = account)
    return render(request,'myapp/accountNum.html',{'customer':customer})

def mainPage(request,customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    return render(request,'myapp/main.html',{'customer':customer})

def loginPage(request):
    allcustomer = Customer.objects.all()
    context = {}
    if request.method=='POST':
        username = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        aadhar_no = request.POST.get('Aadhar_no')
        password = request.POST.get('password')
        for customer in allcustomer:
            if customer.name == username and customer.phone_no == phone_no and customer.Aadhar_no ==aadhar_no and customer.password == password:
                return redirect(f'/main/{customer.customer_id}')
        context['invalid_credentials'] = True 
                
        
    return render(request,'myapp/loginpage.html',context)

def checkBalance(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details = Account.objects.get(account_number=account)
    return render(request,'myapp/checkbalance.html',{'customer':customer,'account_details':account_details})

def deposit(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details = Account.objects.get(account_number=account)
    if request.method == 'POST':
        amount = request.POST.get('deposit')
        account_details.balance += float(amount)
        return redirect(request,f'/main/{customer.customer_id}')
    return render(request,'myapp/deposit.html',{'customer':customer,'account_details':account_details})


    
    

