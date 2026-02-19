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


# Role Views
def role_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    # Get all roles with pagination
    from core.models import Role
    roles_list = Role.objects.all().order_by('-id')
    
    items_per_page = request.GET.get('per_page', 10)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    paginator = Paginator(roles_list, items_per_page)
    page = request.GET.get('page', 1)
    
    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)
    
    current_page = roles.number
    total_pages = paginator.num_pages
    
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
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'roles': roles,
        'page_range': page_range,
        'total_pages': total_pages,
        'items_per_page': items_per_page,
    }
    return render(request, 'role.html', context)


def role_add_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Role
    
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        role_description = request.POST.get('role_description')
        
        Role.objects.create(
            role_name=role_name,
            role_description=role_description,
            is_active=1
        )
        return redirect('role')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
    }
    return render(request, 'role_add.html', context)


def role_edit_view(request, role_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Role
    
    role = Role.objects.get(id=role_id)
    
    if request.method == 'POST':
        role.role_name = request.POST.get('role_name')
        role.role_description = request.POST.get('role_description')
        role.save()
        return redirect('role')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'role': role,
    }
    return render(request, 'role_edit.html', context)


def role_delete_view(request, role_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Role
    
    role = Role.objects.get(id=role_id)
    role.delete()
    return redirect('role')


# Role Permission Views
def role_permission_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Role, Page, RolePermission
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    roles = Role.objects.all()
    pages = Page.objects.filter(is_active=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'roles': roles,
        'pages': pages,
    }
    return render(request, 'role_permission.html', context)


def role_permission_edit_view(request, role_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Role, Page, RolePermission
    
    role = Role.objects.get(id=role_id)
    pages = Page.objects.filter(is_active=1)
    
    if request.method == 'POST':
        for page in pages:
            page_id = str(page.id)
            can_view = 1 if request.POST.get(f'can_view_{page_id}') else 0
            can_add = 1 if request.POST.get(f'can_add_{page_id}') else 0
            can_edit = 1 if request.POST.get(f'can_edit_{page_id}') else 0
            can_delete = 1 if request.POST.get(f'can_delete_{page_id}') else 0
            
            RolePermission.objects.update_or_create(
                role=role,
                page=page,
                defaults={
                    'can_view': can_view,
                    'can_add': can_add,
                    'can_edit': can_edit,
                    'can_delete': can_delete,
                    'is_active': 1
                }
            )
        return redirect('role_permission')
    
    # Get existing permissions
    permissions = RolePermission.objects.filter(role=role)
    permission_dict = {p.page_id: p for p in permissions}
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'role': role,
        'pages': pages,
        'permissions': permission_dict,
    }
    return render(request, 'role_permission_edit.html', context)


# Page Views
def page_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Page
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    pages_list = Page.objects.all().order_by('-id')
    
    items_per_page = request.GET.get('per_page', 10)
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    paginator = Paginator(pages_list, items_per_page)
    page = request.GET.get('page', 1)
    
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    current_page = pages.number
    total_pages = paginator.num_pages
    
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
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'pages': pages,
        'page_range': page_range,
        'total_pages': total_pages,
        'items_per_page': items_per_page,
    }
    return render(request, 'page.html', context)


def page_add_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Page
    
    if request.method == 'POST':
        page_name = request.POST.get('page_name')
        page_url = request.POST.get('page_url')
        page_icon = request.POST.get('page_icon')
        
        Page.objects.create(
            page_name=page_name,
            page_url=page_url,
            page_icon=page_icon,
            is_active=1
        )
        return redirect('page')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
    }
    return render(request, 'page_add.html', context)


def page_edit_view(request, page_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Page
    
    page = Page.objects.get(id=page_id)
    
    if request.method == 'POST':
        page.page_name = request.POST.get('page_name')
        page.page_url = request.POST.get('page_url')
        page.page_icon = request.POST.get('page_icon')
        page.save()
        return redirect('page')
    
    all_employees = Employeedetails.objects.all()
    users = User.objects.filter(isactive=1)
    
    context = {
        'employees': all_employees,
        'users': users,
        'username': request.session.get('username'),
        'page': page,
    }
    return render(request, 'page_edit.html', context)


def page_delete_view(request, page_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from core.models import Page
    
    page = Page.objects.get(id=page_id)
    page.delete()
    return redirect('page')
