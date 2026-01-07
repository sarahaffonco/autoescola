from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse 
from django.template.loader import render_to_string 
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
import json

from .forms import (
    UserLoginForm, 
    StudentRegistrationForm, 
    InstructorRegistrationForm, 
    EmployeeRegistrationForm,
    StudentEditForm, 
    InstructorEditForm, 
    InstructorPersonalEditForm,
    StudentPersonalEditForm,
    EmployeeEditForm,
    InstructorVehicleForm,
)
from .models import User, StudentProfile, InstructorProfile, EmployeeProfile, InstructorVehicle


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
    
    # Data de hoje para limitar campos de data
    from datetime import date
    today = date.today()
    
    if request.method == 'POST':
        print("\n=== DEBUG: Iniciando registro de instrutor ===")
        print(f"POST data: {request.POST.keys()}")
        print(f"FILES data: {request.FILES.keys()}")
        
        form = InstructorRegistrationForm(request.POST, request.FILES)
        print(f"Form criado, validando...")
        
        if form.is_valid():
            print(f"Form válido! cleaned_data: {form.cleaned_data.keys()}")
            try:
                print("Chamando form.save()...")
                user = form.save()
                print(f"Usuário criado: {user.username} (ID: {user.id})")
                login(request, user)
                messages.success(request, 'Conta de instrutor criada com sucesso! Aguarde aprovação.')
                return redirect('instrutor_dashboard')
            except Exception as e:
                import traceback
                print(f'\n!!! ERRO AO CADASTRAR INSTRUTOR: {str(e)} !!!')
                print(f'Tipo do erro: {type(e).__name__}')
                traceback.print_exc()
                messages.error(request, f'Erro ao criar conta: {str(e)}')
                # Retorna o formulário com os dados para reedição
                return render(request, 'accounts/register_instructor.html', {'form': form, 'today': today})
        else:
            # Formulário com erros de validação
            print(f"Form INVÁLIDO! Erros: {form.errors}")
            for field, errors in form.errors.items():
                print(f"  - {field}: {errors}")
            return render(request, 'accounts/register_instructor.html', {'form': form, 'today': today})
    else:
        form = InstructorRegistrationForm()
    
    return render(request, 'accounts/register_instructor.html', {'form': form, 'today': today})


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
    
    return render(request, 'core/instrutor.html', context)


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


@login_required
def instructor_vehicle_view(request):
    """Página para visualizar/editar o veículo do instrutor"""
    if not request.user.is_instrutor():
        messages.error(request, 'Acesso não autorizado')
        return redirect('login')

    profile = request.user.get_profile()
    if not profile or not isinstance(profile, InstructorProfile):
        messages.error(request, 'Perfil de instrutor não encontrado.')
        return redirect('instrutor_dashboard')

    vehicles = profile.vehicles.all().order_by('-id')
    editing_vehicle = None

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        if vehicle_id:
            editing_vehicle = vehicles.filter(id=vehicle_id).first()

        form = InstructorVehicleForm(request.POST, instance=editing_vehicle)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.instructor = profile
            entity.save()
            action = request.POST.get('action')
            message_text = 'Veículo atualizado com sucesso!' if editing_vehicle else 'Veículo cadastrado com sucesso!'
            messages.success(request, message_text)
            if action == 'save_add_another':
                return redirect('instructor_vehicle')
            return redirect('instrutor_dashboard')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        vehicle_id = request.GET.get('vehicle_id')
        if vehicle_id:
            editing_vehicle = vehicles.filter(id=vehicle_id).first()
        form = InstructorVehicleForm(instance=editing_vehicle)

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
        'vehicles': vehicles,
        'editing_vehicle': editing_vehicle,
        'title': 'Veículo do Instrutor'
    }

    return render(request, 'accounts/edit_vehicle.html', context)


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
        # Para alunos, garante que buscamos o perfil real (OneToOne usa related_name diferente)
        profile = user.get_profile()
        if profile and not isinstance(profile, StudentProfile):
            profile = StudentProfile.objects.filter(user=user).first()
        
        # 2. Tratamento do GET (Carregar Formulário)
        if request.method == 'GET':
            form = StudentPersonalEditForm(user=user, profile=profile)
            html = render_to_string('accounts/edit_student_personal.html', {
                'form': form, 
                'user': user,
                'profile': profile
            }, request=request)
            return HttpResponse(html)
        
        # 3. Tratamento do POST (Salvar Dados)
        elif request.method == 'POST':
            form = StudentPersonalEditForm(request.POST, request.FILES, user=user, profile=profile)
            
            try:
                if form.is_valid():
                    result = form.save()
                    
                    # Extrai informações do resultado
                    saved_user = result.get('user') if isinstance(result, dict) else result
                    cancelled_lessons = result.get('cancelled_lessons', 0) if isinstance(result, dict) else 0

                    # Garante a URL absoluta mais recente da foto para atualizar o avatar do usuário
                    profile = saved_user.get_profile()
                    photo_url = None
                    if profile and getattr(profile, 'photo', None):
                        profile.refresh_from_db()
                        version = int(timezone.now().timestamp())
                        photo_url = f"{request.build_absolute_uri(profile.photo.url)}?v={version}"

                    # Mensagem personalizada se houve cancelamento de aulas
                    message = 'Dados atualizados com sucesso!'
                    if cancelled_lessons > 0:
                        message = f'Dados atualizados! {cancelled_lessons} aula(s) cancelada(s) devido à mudança de endereço. Por favor, agende novas aulas.'

                    return JsonResponse({
                        'success': True,
                        'message': message,
                        'photo_url': photo_url,
                        'cancelled_lessons': cancelled_lessons,
                        'full_name': saved_user.full_name,
                        'username': saved_user.username
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
                    'message': f'Erro ao salvar: {str(e)}'
                }, status=500)
            
            
            
    elif role == 'instrutor':
        # Para instrutores, usa o formulário simplificado de dados pessoais
        profile = user.get_profile()
        if profile and not isinstance(profile, InstructorProfile):
            profile = InstructorProfile.objects.filter(user=user).first()
        
        # 2. Tratamento do GET (Carregar Formulário)
        if request.method == 'GET':
            form = InstructorPersonalEditForm(user=user, profile=profile)
            html = render_to_string('accounts/edit_instructor_personal.html', {
                'form': form, 
                'user': user,
                'profile': profile
            }, request=request)
            return HttpResponse(html)
        
        # 3. Tratamento do POST (Salvar Dados)
        elif request.method == 'POST':
            form = InstructorPersonalEditForm(request.POST, request.FILES, user=user, profile=profile)
            
            try:
                if form.is_valid():
                    form.save()

                    # Garante a URL absoluta mais recente da foto para atualizar o avatar do usuário
                    profile = user.get_profile()
                    photo_url = None
                    if profile and getattr(profile, 'photo', None):
                        profile.refresh_from_db()
                        version = int(timezone.now().timestamp())
                        photo_url = f"{request.build_absolute_uri(profile.photo.url)}?v={version}"

                    return JsonResponse({
                        'success': True,
                        'message': 'Dados atualizados com sucesso!',
                        'photo_url': photo_url,
                        'full_name': user.full_name,
                        'username': user.username
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
                    'message': f'Erro ao salvar: {str(e)}'
                }, status=500)
            
    elif role == 'funcionario':
        profile = user.get_profile()
        if profile and not isinstance(profile, EmployeeProfile):
            profile = EmployeeProfile.objects.filter(user=user).first()

        form_class = EmployeeEditForm
        instance = profile or EmployeeProfile(user=user)
        template = 'accounts/edit_employee.html'
    else:
        # Se não tiver role definido
        return JsonResponse({
            'success': False, 
            'message': 'Tipo de usuário não reconhecido.'
        }, status=400)

    # Fluxo original apenas para funcionário
    if role in ['funcionario']:
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
                return JsonResponse({
                    'success': False,
                    'message': f'Erro ao salvar: {str(e)}'
                }, status=500)