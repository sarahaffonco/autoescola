from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import User, InstructorProfile, EmployeeProfile
from datetime import date
import json


@csrf_exempt
def register_api_instrutor(request):
    """API para cadastro de instrutor via JSON ou FormData"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    # Detecta se é JSON ou FormData
    if request.content_type and 'application/json' in request.content_type:
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            full_name = data.get('full_name', '').strip()
            phone = data.get('phone', '').strip()
            photo = None
        except:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        # FormData
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        photo = request.FILES.get('photo')
    
    # Validação básica
    errors = {}
    
    if not email:
        errors['email'] = 'Email é obrigatório'
    elif User.objects.filter(email=email).exists():
        errors['email'] = 'Este email já está cadastrado'
    
    if not password:
        errors['password'] = 'Senha é obrigatória'
    elif len(password) < 6:
        errors['password'] = 'Senha deve ter pelo menos 6 caracteres'
    
    if not full_name:
        errors['full_name'] = 'Nome completo é obrigatório'
    elif len(full_name) < 2:
        errors['full_name'] = 'Nome deve ter pelo menos 2 caracteres'
    
    if not phone:
        errors['phone'] = 'Telefone é obrigatório'
    elif len(phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
        errors['phone'] = 'Telefone inválido. Use o formato (XX) XXXXX-XXXX'
    
    # Validação de foto se fornecida
    if photo:
        ext = photo.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            errors['photo'] = f'Formato de arquivo não permitido: {ext}. Use apenas JPG, JPEG ou PNG'
        elif photo.size > 5 * 1024 * 1024:  # 5MB
            errors['photo'] = 'Arquivo muito grande. Máximo: 5MB'
    
    if errors:
        return JsonResponse({
            'error': 'Erro na validação',
            'errors': errors
        }, status=400)
    
    # Cria o usuário
    try:
        # Gera username único
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role='instrutor'
        )
        
        # Cria o perfil do instrutor com dados mínimos
        InstructorProfile.objects.create(
            user=user,
            phone=phone,
            status='pendente',
            # Dados mínimos obrigatórios
            cpf=f'{user.id:011d}',  # CPF único baseado no ID do usuário
            rg=f'{user.id:011d}',  # RG único baseado no ID
            cnh=f'{user.id:011d}',  # CNH única baseada no ID
            birth_date=date(1990, 1, 1),  # Data de nascimento mínima
            cnh_emission_date=date(2010, 1, 1),  # Data de emissão mínima
            credential=f'TEMP{user.id:06d}',  # Credencial único baseado no ID
            cep='00000000',  # Placeholder
            address='Não informado',
            address_number='0',
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Instrutor cadastrado com sucesso!'
        })
    
    except Exception as e:
        return JsonResponse({
            'error': f'Erro ao criar conta: {str(e)}'
        }, status=500)


@csrf_exempt
def register_api_funcionario(request):
    """API para cadastro de funcionário via JSON ou FormData"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    # Detecta se é JSON ou FormData
    if request.content_type and 'application/json' in request.content_type:
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            full_name = data.get('full_name', '').strip()
            phone = data.get('phone', '').strip()
            photo = None
        except:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        # FormData
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        photo = request.FILES.get('photo')
    
    # Validação básica
    errors = {}
    
    if not email:
        errors['email'] = 'Email é obrigatório'
    elif User.objects.filter(email=email).exists():
        errors['email'] = 'Este email já está cadastrado'
    
    if not password:
        errors['password'] = 'Senha é obrigatória'
    elif len(password) < 6:
        errors['password'] = 'Senha deve ter pelo menos 6 caracteres'
    
    if not full_name:
        errors['full_name'] = 'Nome completo é obrigatório'
    elif len(full_name) < 2:
        errors['full_name'] = 'Nome deve ter pelo menos 2 caracteres'
    
    if not phone:
        errors['phone'] = 'Telefone é obrigatório'
    elif len(phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
        errors['phone'] = 'Telefone inválido. Use o formato (XX) XXXXX-XXXX'
    
    # Validação de foto se fornecida
    if photo:
        ext = photo.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            errors['photo'] = f'Formato de arquivo não permitido: {ext}. Use apenas JPG, JPEG ou PNG'
        elif photo.size > 5 * 1024 * 1024:  # 5MB
            errors['photo'] = 'Arquivo muito grande. Máximo: 5MB'
    
    if errors:
        return JsonResponse({
            'error': 'Erro na validação',
            'errors': errors
        }, status=400)
    
    # Cria o usuário
    try:
        # Gera username único
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role='funcionario'
        )
        
        # Cria o perfil do funcionário
        EmployeeProfile.objects.create(
            user=user,
            phone=phone
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Funcionário cadastrado com sucesso!'
        })
    
    except Exception as e:
        return JsonResponse({
            'error': f'Erro ao criar conta: {str(e)}'
        }, status=500)


@csrf_exempt
def login_api(request):
    """API para login via JSON"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return JsonResponse({
            'error': 'Email e senha são obrigatórios'
        }, status=400)
    
    try:
        user = User.objects.get(email=email)
        user_auth = authenticate(username=user.username, password=password)
        
        if user_auth:
            login(request, user_auth)
            return JsonResponse({
                'success': True,
                'message': 'Login realizado com sucesso!'
            })
        else:
            return JsonResponse({
                'error': 'Email ou senha inválidos'
            }, status=401)
    
    except User.DoesNotExist:
        return JsonResponse({
            'error': 'Email ou senha inválidos'
        }, status=401)
    except Exception as e:
        return JsonResponse({
            'error': f'Erro ao fazer login: {str(e)}'
        }, status=500)


@csrf_exempt
def me_api(request):
    """API para obter dados do usuário autenticado"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
    
    return JsonResponse({
        'id': request.user.id,
        'email': request.user.email,
        'full_name': request.user.full_name,
        'role': request.user.role
    })


@csrf_exempt
def register_api_aluno(request):
    """API para cadastro de aluno via JSON ou FormData"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    # Detecta se é JSON ou FormData
    if request.content_type and 'application/json' in request.content_type:
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            full_name = data.get('full_name', '').strip()
            phone = data.get('phone', '').strip()
            photo = None
        except:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        # FormData
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        photo = request.FILES.get('photo')
    
    # Validação básica
    errors = {}
    
    if not email:
        errors['email'] = 'Email é obrigatório'
    elif User.objects.filter(email=email).exists():
        errors['email'] = 'Este email já está cadastrado'
    
    if not password:
        errors['password'] = 'Senha é obrigatória'
    elif len(password) < 6:
        errors['password'] = 'Senha deve ter pelo menos 6 caracteres'
    
    if not full_name:
        errors['full_name'] = 'Nome completo é obrigatório'
    elif len(full_name) < 2:
        errors['full_name'] = 'Nome deve ter pelo menos 2 caracteres'
    
    if not phone:
        errors['phone'] = 'Telefone é obrigatório'
    elif len(phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
        errors['phone'] = 'Telefone inválido. Use o formato (XX) XXXXX-XXXX'
    
    # Validação de foto se fornecida
    if photo:
        ext = photo.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            errors['photo'] = f'Formato de arquivo não permitido: {ext}. Use apenas JPG, JPEG ou PNG'
        elif photo.size > 5 * 1024 * 1024:  # 5MB
            errors['photo'] = 'Arquivo muito grande. Máximo: 5MB'
    
    if errors:
        return JsonResponse({
            'error': 'Erro na validação',
            'errors': errors
        }, status=400)
    
    # Cria o usuário
    try:
        # Gera username único
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role='aluno'
        )
        
        # Cria o perfil do aluno com dados mínimos
        from .models import StudentProfile
        StudentProfile.objects.create(
            user=user,
            phone=phone,
            # Dados mínimos obrigatórios
            cpf=f'{user.id:011d}',  # CPF único baseado no ID do usuário
            rg=f'{user.id:011d}',  # RG único baseado no ID
            cep='00000000',  # Placeholder
            address='Não informado',
            address_number='0',
            birth_date=date(1990, 1, 1),  # Data de nascimento mínima
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Aluno cadastrado com sucesso!'
        })
    
    except Exception as e:
        return JsonResponse({
            'error': f'Erro ao criar conta: {str(e)}'
        }, status=500)


@csrf_exempt
def logout_api(request):
    """API para fazer logout"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Logout realizado com sucesso!'
    })
