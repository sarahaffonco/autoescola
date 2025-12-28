from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect('instrutor_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Try to get user by email
            from .models import User
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('instrutor_dashboard' if user.role == 'instrutor' else 'aluno_dashboard')
                else:
                    messages.error(request, 'Email ou senha incorretos')
            except User.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def choice_view(request):
    """View para escolher o tipo de cadastro"""
    if request.user.is_authenticated:
        return redirect('instrutor_dashboard')
    
    return render(request, 'accounts/choice.html')

def register_student_view(request):
    """Cadastro específico para aluno"""
    return register_role_view(request, 'aluno', 'accounts/register_student.html')

def register_instructor_view(request):
    """Cadastro específico para instrutor"""
    return register_role_view(request, 'instrutor', 'accounts/register_instructor.html')

def register_employee_view(request):
    """Cadastro específico para funcionário"""
    return register_role_view(request, 'funcionario', 'accounts/register_employee.html')

def register_role_view(request, role, template_name):
    """Função genérica para registro com role específico"""
    if request.user.is_authenticated:
        return redirect('instrutor_dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role  # Define o role específico
            user.save()
            login(request, user)
            messages.success(request, f'Conta de {role} criada com sucesso!')
            return redirect('instrutor_dashboard' if user.role == 'instrutor' else 'aluno_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, template_name, {'form': form, 'role': role})

def register_view(request):
    """Redireciona para a página de choice"""
    return redirect('choice')

@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('login')