from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse  # ← ADICIONE HttpResponse
from django.template.loader import render_to_string  # ← ADICIONE render_to_string

from .forms import (
    UserLoginForm, 
    StudentRegistrationForm, 
    InstructorRegistrationForm, 
    EmployeeRegistrationForm,
    StudentEditForm, InstructorEditForm, EmployeeEditForm  # ← Já está aqui
)
from .models import User


def login_view(request):
    """Login view com validações específicas"""
    if request.user.is_authenticated:
        # Redireciona para o dashboard apropriado baseado no role
        if request.user.role == 'instrutor':
            return redirect('instrutor_dashboard')
        elif request.user.role == 'funcionario':
            return redirect('funcionario_dashboard')
        else:
            return redirect('aluno_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user_auth = authenticate(username=user.username, password=password)
                
                if user_auth:
                    login(request, user_auth)
                    # Redireciona baseado no role
                    if user_auth.role == 'instrutor':
                        return redirect('instrutor_dashboard')
                    elif user_auth.role == 'funcionario':
                        return redirect('funcionario_dashboard')
                    else:
                        return redirect('aluno_dashboard')
                
            except User.DoesNotExist:
                # Isso já foi tratado no formulário
                pass
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


# ============================================
# VIEWS PARA EDITAR PERFIL 
# ============================================



@login_required
def edit_profile_view(request):
    """View para edição de perfil (AJAX)"""
    if request.method == 'GET':
        # Retorna o formulário apropriado
        user = request.user
        profile = user.get_profile()
        
        if user.role == 'aluno' and hasattr(user, 'studentprofile'):
            form = StudentEditForm(instance=user.studentprofile)
            template = 'accounts/edit_student.html'
        elif user.role == 'instrutor' and hasattr(user, 'instructorprofile'):
            form = InstructorEditForm(instance=user.instructorprofile)
            template = 'accounts/edit_instructor.html'
        elif user.role == 'funcionario' and hasattr(user, 'employeeprofile'):
            form = EmployeeEditForm(instance=user.employeeprofile)
            template = 'accounts/edit_employee.html'
        else:
            return JsonResponse({'error': 'Perfil não encontrado'}, status=404)
        
        # Renderiza o template apropriado
        html = render_to_string(template, {'form': form, 'user': user}, request=request)
        return HttpResponse(html)
    
    elif request.method == 'POST':
        # Processa o formulário de edição
        user = request.user
        profile = user.get_profile()
        
        try:
            if user.role == 'aluno' and hasattr(user, 'studentprofile'):
                form = StudentEditForm(request.POST, request.FILES, instance=user.studentprofile)
            elif user.role == 'instrutor' and hasattr(user, 'instructorprofile'):
                form = InstructorEditForm(request.POST, request.FILES, instance=user.instructorprofile)
            elif user.role == 'funcionario' and hasattr(user, 'employeeprofile'):
                form = EmployeeEditForm(request.POST, request.FILES, instance=user.employeeprofile)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Perfil não encontrado'
                }, status=404)
            
            if form.is_valid():
                form.save()
                
                # Atualiza também o usuário se necessário
                if 'email' in form.cleaned_data:
                    user.email = form.cleaned_data['email']
                    user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cadastro atualizado com sucesso!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor, corrija os erros abaixo.',
                    'errors': form.errors
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar cadastro: {str(e)}'
            }, status=500)