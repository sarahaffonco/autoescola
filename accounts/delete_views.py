from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.urls import reverse


@login_required
def delete_account_view(request):
    """Permite exclusão de cadastro com dupla confirmação.
    Requer: senha atual válida, texto de confirmação 'EXCLUIR' e ciência de irreversibilidade.
    Retorna JSON com instruções de redirecionamento.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    user = request.user
    password = (request.POST.get('password') or '').strip()
    confirm_text = (request.POST.get('confirm_text') or '').strip().upper()
    ack = (request.POST.get('ack') or '').strip().lower() in ['1', 'true', 'on', 'yes', 'sim']

    errors = {}
    if not ack:
        errors['ack'] = 'Você deve confirmar que a exclusão é irreversível.'
    if confirm_text != 'EXCLUIR':
        errors['confirm_text'] = "Digite 'EXCLUIR' para confirmar."
    if not user.check_password(password):
        errors['password'] = 'Senha atual incorreta.'

    if errors:
        return JsonResponse({'success': False, 'message': 'Validação falhou.', 'errors': errors}, status=400)

    # Encerrar sessão antes de excluir para evitar estado inconsistente
    try:
        logout(request)
    except Exception:
        # Mesmo se falhar, continuamos com exclusão do usuário
        pass

    # Excluir usuário (perfis relacionados serão removidos via CASCADE)
    try:
        user.delete()
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao excluir: {str(e)}'}, status=500)

    return JsonResponse({
        'success': True,
        'message': 'Cadastro excluído com sucesso. Esta ação é irreversível.',
        'redirect_url': reverse('login')
    })
