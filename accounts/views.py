from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse 
from django.template.loader import render_to_string 

from .forms import (
    UserLoginForm, 
    StudentRegistrationForm, 
    InstructorRegistrationForm, 
    EmployeeRegistrationForm,
    StudentEditForm, 
    InstructorEditForm, 
    EmployeeEditForm,
    StudentProfile,         
    InstructorProfile,      
    EmployeeProfile            
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
    """View centralizada para edição de perfil via AJAX"""
    user = request.user
    role = str(user.role).lower() if user.role else ""
    
    form_class = None
    instance = None
    template = None

    # 1. Identificação do Perfil
    if role == 'aluno':
        if hasattr(user, 'studentprofile'):
            form_class = StudentEditForm
            instance = user.studentprofile
            template = 'accounts/edit_student.html'
        else:
            # Cria um perfil vazio se não existir
            instance = StudentProfile(user=user)
            form_class = StudentEditForm
            template = 'accounts/edit_student.html'
            
    elif role == 'instrutor':
        if hasattr(user, 'instructorprofile'):
            form_class = InstructorEditForm
            instance = user.instructorprofile
            template = 'accounts/edit_instructor.html'
        else:
            # Cria um perfil vazio se não existir
            instance = InstructorProfile(user=user)
            form_class = InstructorEditForm
            template = 'accounts/edit_instructor.html'
            
    elif role == 'funcionario':
        if hasattr(user, 'employeeprofile'):
            form_class = EmployeeEditForm
            instance = user.employeeprofile
            template = 'accounts/edit_employee.html'
        else:
            # Cria um perfil vazio se não existir
            instance = EmployeeProfile(user=user)
            form_class = EmployeeEditForm
            template = 'accounts/edit_employee.html'
    else:
        # Se não tiver role definido
        return JsonResponse({
            'success': False, 
            'message': 'Tipo de usuário não reconhecido.'
        }, status=400)

    # 2. Tratamento do GET (Carregar Formulário)
    if request.method == 'GET':
        form = form_class(instance=instance)
        
        # Preenche campos básicos do User se o perfil for novo
        if not instance.pk:  # Se for um perfil novo/não salvo
            form.initial = {
                'full_name': user.full_name or user.username,
                'email': user.email,
                'phone': user.phone or '',
            }
        
        html = render_to_string(template, {'form': form, 'user': user}, request=request)
        return HttpResponse(html)

    # 3. Tratamento do POST (Salvar Dados)
    elif request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        
        try:
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user  # Garante a relação
                profile.save()
                
                # Sincroniza o e-mail com o modelo User
                if 'email' in form.cleaned_data:
                    user.email = form.cleaned_data['email']
                if 'full_name' in form.cleaned_data:
                    user.full_name = form.cleaned_data['full_name']
                if 'phone' in form.cleaned_data:
                    user.phone = form.cleaned_data['phone']
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
            print(f"Erro ao salvar perfil: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar: {str(e)}'
            }, status=500)