from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import User


def password_reset_request(request):
    """API endpoint para solicitar reset de senha via email"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            
            if not email:
                return JsonResponse({'success': False, 'error': 'Email é obrigatório.'}, status=400)
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'success': True})
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = request.build_absolute_uri(
                f'/auth/password-reset-confirm/{uid}/{token}/'
            )
            
            subject = 'Recuperação de Senha - AutoEscola'
            message = f"""
Olá {user.full_name or user.username},

Você solicitou a recuperação de senha da sua conta na AutoEscola.

Clique no link abaixo para redefinir sua senha:
{reset_link}

Este link é válido por 24 horas.

Se você não solicitou esta recuperação, ignore este email.

Atenciosamente,
Equipe AutoEscola
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'success': True})
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
                return JsonResponse({
                    'success': False,
                    'error': 'Erro ao enviar email. Tente novamente.'
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Dados inválidos.'}, status=400)
        except Exception as e:
            print(f"Erro no password reset: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Erro ao processar solicitação.'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)


def password_reset_confirm(request, uidb64, token):
    """View para confirmar reset de senha com token"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    validlink = user is not None and default_token_generator.check_token(user, token)
    
    if request.method == 'POST' and validlink:
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        
        if password1 and password2:
            if password1 == password2:
                if len(password1) >= 8:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Senha redefinida com sucesso! Faça login com sua nova senha.')
                    return redirect('login')
                else:
                    messages.error(request, 'A senha deve ter no mínimo 8 caracteres.')
            else:
                messages.error(request, 'As senhas não coincidem.')
        else:
            messages.error(request, 'Preencha todos os campos.')
    
    return render(request, 'accounts/password_reset_confirm.html', {
        'validlink': validlink,
        'user': user
    })
