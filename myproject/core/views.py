from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Employeedetails, User


def login_view(request):
    # If already logged in, redirect to dashboard
    if request.session.get('user_id'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists in User table (database first approach)
        try:
            user = User.objects.get(username=username, password=password, isactive=1)
            # Store user info in session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        except User.MultipleObjectsReturned:
            return render(request, 'login.html', {'error': 'Multiple users found. Please contact administrator.'})
    
    return render(request, 'login.html')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
    }
    return render(request, 'dashboard.html', context)


def employees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Get all employees and add pagination
    employees_list = Employeedetails.objects.all().order_by('id')
    
    # Get items per page from query params, default to 10
    items_per_page = request.GET.get('per_page', 10)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    # Create paginator
    paginator = Paginator(employees_list, items_per_page)
    
    # Get current page number
    page = request.GET.get('page', 1)
    
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    
    users = User.objects.filter(isactive=1)
    
    # Build pagination range
    current_page = employees.number
    total_pages = paginator.num_pages
    
    # Get page range (show at most 5 pages)
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if current_page <= 3:
            page_range = range(1, 6)
        elif current_page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)
    
    context = {
        'employees': employees,
        'users': users,
        'username': request.session.get('username'),
        'page_range': page_range,
        'total_pages': total_pages,
        'items_per_page': items_per_page,
    }
    return render(request, 'employees.html', context)


def users_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Get all users and add pagination
    users_list = User.objects.filter(isactive=1).order_by('id')
    
    # Get items per page from query params, default to 10
    items_per_page = request.GET.get('per_page', 10)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    # Create paginator
    paginator = Paginator(users_list, items_per_page)
    
    # Get current page number
    page = request.GET.get('page', 1)
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    all_employees = Employeedetails.objects.all()
    
    # Build pagination range
    current_page = users.number
    total_pages = paginator.num_pages
    
    # Get page range (show at most 5 pages)
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if current_page <= 3:
            page_range = range(1, 6)
        elif current_page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)
    
    context = {
        'users': users,
        'employees': all_employees,
        'username': request.session.get('username'),
        'page_range': page_range,
        'total_pages': total_pages,
        'items_per_page': items_per_page,
    }
    return render(request, 'users.html', context)


def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    current_user = User.objects.filter(id=request.session.get('user_id'), isactive=1).first()
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'current_user': current_user,
    }
    return render(request, 'profile.html', context)


def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
    }
    return render(request, 'settings.html', context)


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')
