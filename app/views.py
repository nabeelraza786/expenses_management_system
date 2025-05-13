from django.shortcuts import render,redirect , get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages # type: ignore
from .models import Client_details, add_providers_details, Expense , Funds
from django.db import IntegrityError
from decimal import Decimal
from django.db.models import Sum , Q
import datetime
from django.contrib.auth.decorators import login_required # type: ignore
from functools import wraps
# Create your views here.
# user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user) # type: ignore
            return redirect('base')
        else:
            messages.error(request , 'Invalid Username and password')
    return render(request,'login.html')
# user logout
def logout_user(request):
    logout(request)
    return redirect('login')

# function for if user is login or not 
def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'page_not_found.html', status=401)  # or custom template
    return wrapper
# base file loading 
@custom_login_required
def Base(request):
    return render(request, 'base.html')


#  show client function
@custom_login_required
def Client(request):
    return render(request, 'client.html')


# add new clients function
@custom_login_required
def add_new_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cif = request.POST.get('cif')
        direction = request.POST.get('direction')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        province = request.POST.get('province')
        phone = request.POST.get('phone')
        email = request.POST.get('email')


        # Debugging: Check the received data , data will be print at the console
        print(f"Received Data: Name={name}, CIF={cif},Direction={direction},postal_code={postal_code},city={city} Email={email}")

        # Check if client email exists (only if email is not empty)
        if email and Client_details.objects.filter(email=email).exists():
            return render(request, 'add_new_client.html', {'error': 'Email already exists!'})

        try:
            Client_details.objects.create(
                name=name,
                cif_nif=cif,
                direction=direction,
                postal_code=postal_code,
                city=city,
                province=province,
                phone=phone,
                email=email,    
            )
            return redirect('all_clients')  # Redirect after successful save

        except IntegrityError:
            return render(request, 'add_new_client.html', {'error': 'Failed to add client due to a database error!'})

    return render(request, 'add_new_client.html')

# delet client function
@custom_login_required
def delet_client(request, client_id):
    client = get_object_or_404(Client_details,id=client_id)
    if request.method == "POST":
     client.delete()
    messages.success(request, "Client deleted successfully.")
    return redirect('all_clients')

# show all clients function
@custom_login_required
def All_clients(request):
   
   # search client 
   query = request.GET.get('search')
   if query:
       client_search = Client_details.objects.filter(name__icontains=query)
   else:
       client_search = Client_details.objects.all()
   clients = Client_details.objects.all()
   client_data = []
   expenses = 0
   received = 0
   balance_total =  0
   for client in clients:
       # Calculate total expenses
       total_expenses = client.expense_set.aggregate(total=Sum('total'))['total'] or 0
       # Calculate total received founds
       total_received = Funds.objects.filter(client=client).aggregate(total=Sum('total'))['total'] or 0
       # Calculate balance
       balance = total_received - total_expenses
    #    if balance  < 0 :
    #        balance = 0
           
      #    when client add funds or expenses it will added in expenses and recevied field and + them all
       expenses += total_expenses
       received += total_received
       balance_total += balance
       client_data.append({
            'id': client.id,
            'name': client.name,
            'direction': client.direction,
            'total_expenses': total_expenses,
            'total_received': total_received,
            'balance': balance,
            'client_search' : client_search,
        })
       
   context = {
       "client_data" : client_data,
       "expenses" : expenses,
       "received" : received,
       "balance_total" : balance_total
    }
       

   return render(request, 'all_clients.html', context)

# show history of client with details
@custom_login_required
def client_history(request,client_id):
    client = get_object_or_404(Client_details, id=client_id)
    expenses = Expense.objects.filter(client_id=client_id).order_by('-date')
    # retrieve the funds of clients 
    funds_recevied = Funds.objects.filter(client_id= client_id).order_by('-date')
    # calculate total sum of all fields 
    total_sum = expenses.aggregate(total_sum=Sum('total'))['total_sum'] or 0
    #  calculate the total sum of all fields funds 
    tsf =funds_recevied.aggregate(tsf=Sum('total'))['tsf'] or 0

    # Calculate remaining balance
    remaining_balance = tsf - total_sum

    context = {
        'client': client,
        'expenses': expenses,
        'total_sum': total_sum,
        'funds_recevied' : funds_recevied,
        'tsf' : tsf,
        'remaining_balance' : remaining_balance,
    }

    return render(request , 'client_history.html',context)

# # function for total expenses per user. tepu=total expenses per user. sepu = sum expenses 
# def tepu(request,client_id):
#     client = get_object_or_404(Client_details, id=client_id)
#     sepu = Expense.objects.filter(client_id=client_id).order_by('-date')

#     context = {
#         'client': client,
#         'sepu': sepu
#     }

#     return render(request , 'client_history.html',context)

# show client balance 
@custom_login_required
def Client_balance(request):
    return render(request , 'client_balance.html')



# show sum of all ammount with tex
@custom_login_required
def Expenses(request):
    expenses = Expense.objects.all()
    total_neto = sum(expense.neto for expense in expenses)
    total_iva = sum(expense.iva for expense in expenses)
    total_total = sum(expense.total for expense in expenses)
    
    return render (request, 'expenses.html',
                   {'expenses' : expenses,
                    'total_neto' : total_neto,
                    'total_iva' : total_iva,
                    'total_total' : total_total})

# def Exp_p_user(request):
#     exp_p = Expense.objects.id.order_by(id)
#     total_net = sum(exp.neto for exp in exp_p )
#     total_

    

# function render total pages
@custom_login_required
def Total_page(request):
    return render (request, 'total_page.html')

# function show all the pages 
@custom_login_required
def all_page(request):
    return render (request, 'all_pages.html')
# add expenses function
@custom_login_required
def add_exp(request):
    # Fetch the available providers and clients to display in the form
    providers = add_providers_details.objects.all()
    clients = Client_details.objects.all()

    # save the expenses details
    if request.method == "POST":
        date = request.POST.get('date')
        provider_id = request.POST.get('provider_id')
        bill_no = request.POST.get('bill_no')
        client_id = request.POST.get('client_id')
        concept = request.POST.get('concept')
        neto = float(request.POST.get('neto')or 0)
        include_iva= request.POST.get('include_iva')#calculate the iva
        # calculate the iva and total based on the user choise 
        if include_iva == "on":
            iva = round(neto * 0.21 , 2)
        else:
            iva = 0.0
        total = round(neto + iva , 2)

        Expense.objects.create(
            date=date,
            provider_id=provider_id,
            bill_no=bill_no,
            client_id=client_id,
            concept= concept,
            neto= neto,
            iva=iva,
            total=total
        )
        messages.success(request, "Expense add successfully")
        return redirect("expenses")
    
    return render (request, 'add_expenses.html', {'providers': providers, 'clients': clients})




# add fund function
@custom_login_required
def add_funds(request):
    # get the available clients from client model
    clients = Client_details.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        client_id = request.POST.get('client_id')
        bill_no = request.POST.get('bill_no')
        concept = request.POST.get('concept')
        neto =float(request.POST.get('neto') or 0)
        # iva = float(neto) * 0.21 #calculate the iva
        include_iva = request.POST.get('include_iva')
        if include_iva == "on":
            iva = round(neto * 0.21, 2)
        else:
            iva = 0.0
        total = round(neto + iva, 2)
        # total = float(neto) + iva #calculte the  total
        # iva = request.POST.get('iva')
        # total = request.POST.get('total')

        Funds.objects.create(
            date=date,
            bill_no=bill_no,
            client_id=client_id,
            concept= concept,
            neto= neto,
            iva=iva,
            total=total
        )
        messages.success(request, "funds add successfully")
        return redirect("all_funds")
    return render (request, 'add_funds.html',{'clients': clients})

# add provider function
@custom_login_required
def add_Provider(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cif = request.POST.get('cif')
        direction = request.POST.get('direction')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        province = request.POST.get('province')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        account_number = request.POST.get('account_number')

        # Check if client email exists (only if email is not empty)
        if email and add_providers_details.objects.filter(email=email).exists():
            return render(request, 'add_providers.html', {'error': 'Email already exists!'})

        try:
            add_providers_details.objects.create(
                name=name,
                cif_cif=cif,
                direction=direction,
                postal_code = postal_code,
                city=city,
                province=province,
                phone=phone,
                email=email,
                account_number= account_number
               
                
            )
            return redirect('add_provider')  # Redirect after successful save

        except IntegrityError:
            return render(request, 'add_providers.html', {'error': 'Failed to add client due to a database error!'})

    return render(request,'add_providers.html')






# show all provider function
@custom_login_required
def all_providers(request):
    providers = add_providers_details.objects.all()
    context = {'providers': providers} 

    return render(request,'all_provider.html',context)


# show all funds function 
@custom_login_required
def all_funds(request):
    funds = Funds.objects.all()
    context = {'funds' : funds}

    return render(request, 'all_funds.html',context)