from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserLoginForm, 
    StudentRegistrationForm, 
    InstructorRegistrationForm, 
    EmployeeRegistrationForm
)


def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        # Redireciona para o dashboard apropriado baseado no role
        if request.user.role == 'instrutor':
            return redirect('instrutor_dashboard')
        elif request.user.role == 'funcionario':
            return redirect('funcionario_dashboard')  # Você precisará criar esta view
        else:
            return redirect('aluno_dashboard')
    
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
                    # Redireciona baseado no role
                    if user.role == 'instrutor':
                        return redirect('instrutor_dashboard')
                    elif user.role == 'funcionario':
                        return redirect('funcionario_dashboard')
                    else:
                        return redirect('aluno_dashboard')
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
        # Redireciona para o dashboard apropriado
        if request.user.role == 'instrutor':
            return redirect('instrutor_dashboard')
        elif request.user.role == 'funcionario':
            return redirect('funcionario_dashboard')
        else:
            return redirect('aluno_dashboard')
    
    return render(request, 'accounts/choice.html')


def register_student_view(request):
    """Cadastro específico para aluno"""
    if request.user.is_authenticated:
        return redirect('aluno_dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Conta de aluno criada com sucesso!')
                return redirect('aluno_dashboard')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register_student.html', {'form': form})


def register_instructor_view(request):
    """Cadastro específico para instrutor"""
    if request.user.is_authenticated:
        return redirect('instrutor_dashboard')
    
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Conta de instrutor criada com sucesso! Aguarde aprovação.')
                return redirect('instrutor_dashboard')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
    else:
        form = InstructorRegistrationForm()
    
    return render(request, 'accounts/register_instructor.html', {'form': form})


def register_employee_view(request):
    """Cadastro específico para funcionário"""
    if request.user.is_authenticated:
        # Redireciona baseado no role
        if request.user.role == 'funcionario':
            return redirect('funcionario_dashboard')
        elif request.user.role == 'instrutor':
            return redirect('instrutor_dashboard')
        else:
            return redirect('aluno_dashboard')
    
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Conta de funcionário criada com sucesso!')
                return redirect('funcionario_dashboard')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
    else:
        form = EmployeeRegistrationForm()
    
    return render(request, 'accounts/register_employee.html', {'form': form})


def register_view(request):
    """Redireciona para a página de choice"""
    return redirect('choice')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('login')


# ============================================
# VIEWS PARA DASHBOARDS (EXEMPLOS)
# ============================================

@login_required
def aluno_dashboard(request):
    """Dashboard para alunos"""
    if not request.user.is_aluno():
        messages.error(request, 'Acesso não autorizado')
        return redirect('login')
    
    # Obtém o perfil do aluno
    profile = request.user.get_profile()
    
    context = {
        'user': request.user,
        'profile': profile,
        'title': 'Dashboard do Aluno'
    }
    
    return render(request, 'core/aluno_dashboard.html', context)


@login_required
def instrutor_dashboard(request):
    """Dashboard para instrutores"""
    if not request.user.is_instrutor():
        messages.error(request, 'Acesso não autorizado')
        return redirect('login')
    
    # Obtém o perfil do instrutor
    profile = request.user.get_profile()
    
    # Verifica se o instrutor está aprovado
    if profile and profile.status != 'ativo':
        messages.warning(request, 'Seu perfil ainda não foi aprovado. Aguarde a aprovação da administração.')
    
    context = {
        'user': request.user,
        'profile': profile,
        'title': 'Dashboard do Instrutor'
    }
    
    return render(request, 'core/instrutor_dashboard.html', context)


@login_required
def funcionario_dashboard(request):
    """Dashboard para funcionários"""
    if not request.user.is_funcionario():
        messages.error(request, 'Acesso não autorizado')
        return redirect('login')
    
    # Obtém o perfil do funcionário
    profile = request.user.get_profile()
    
    context = {
        'user': request.user,
        'profile': profile,
        'title': 'Dashboard do Funcionário'
    }
    
    return render(request, 'core/funcionario_dashboard.html', context)


# ============================================
# VIEWS PARA PERFIL (OPCIONAIS)
# ============================================

@login_required
def profile_view(request):
    """Visualização e edição do perfil do usuário"""
    profile = request.user.get_profile()
    
    if request.method == 'POST':
        # Aqui você pode adicionar lógica para editar o perfil
        pass
    
    context = {
        'user': request.user,
        'profile': profile,
        'title': 'Meu Perfil'
    }
    
    template_name = f'accounts/profile_{request.user.role}.html'
    
    return render(request, template_name, context)