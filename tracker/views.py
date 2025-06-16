from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from collections import defaultdict
import calendar
# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "Username not found") 
            return redirect('login_view')
        
        user = authenticate(username = username , password = password)
        if not user:
            messages.success(request, "Incorrect password") 
            return redirect('login_view')        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.success(request, "Username is already taken") 
            return redirect('register_view')
        user = User.objects.create(
            username = username,
            first_name = first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created") 
        return redirect('login_view')
    return render(request, 'register.html')
def logout_view(request):
    logout(request)
    return redirect('login_view')  
@login_required(login_url='login_view')
def index(request):
    return render(request, 'index.html')
def dashboard(request):
    transactions = Transaction.objects.all().order_by('-Date')
    recent_transactions = transactions[:5]

   
    total_income = sum(t.Amount for t in transactions if t.Type == 'Income')
    total_expense = sum(t.Amount for t in transactions if t.Type == 'Expense')
    balance = total_income - total_expense

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'recent_transactions': recent_transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })

def reports(request):
    transactions = Transaction.objects.all()

    # PIE CHART DATA
    expense_summary = defaultdict(float)
    for t in transactions.filter(Type="Expense"):
        expense_summary[t.Category] += t.Amount
    expense_data = [{'Category': cat, 'total': total} for cat, total in expense_summary.items()]
    print(expense_data)
    
    monthly = (
    Transaction.objects
    .annotate(month=TruncMonth('Date'))
    .values('month', 'Type')
    .annotate(total=Sum('Amount'))
    )
#BAR CHART DATA
    summary = {}
    for entry in monthly:
        m = entry['month'].strftime('%b %Y')
        if m not in summary:
            summary[m] = {'Income': 0, 'Expense': 0}
        summary[m][entry['Type']] = entry['total']

    monthly_summary = {
    'months': list(summary.keys()),
    'income': [summary[m]['Income'] for m in summary],
    'expense': [summary[m]['Expense'] for m in summary],
}
    print(monthly_summary)

    context = {
        'expense_data_json': json.dumps(expense_data),
        'monthly_summary_json': json.dumps(monthly_summary),
    }
    return render(request, 'reports.html', context)

def history(request):
    transactions = Transaction.objects.all().order_by('-Date')
    search = request.GET.get('search', '')
    trans_type = request.GET.get('type', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    
    if search:
        transactions = transactions.filter(Description__icontains=search)

    if trans_type:
        transactions = transactions.filter(Type=trans_type)

    if category:
        transactions = transactions.filter(Category=category)

    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            transactions = transactions.filter(Date__gte=start)
        except ValueError:
            pass

    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            transactions = transactions.filter(Date__lte=end)
        except ValueError:
            pass

    return render(request, 'history.html', {'transactions': transactions})
from .forms import TransactionForm

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('/add_transaction/')  
    else:
        form = TransactionForm()  
    context = {'form': form}  
    return render(request, 'add_transaction.html', context)
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('/history/') 
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'edit_transaction.html', {'form': form})
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.delete()
    return redirect('history')  
