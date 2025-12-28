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


def register_view(request):
    """Registration view"""
    if request.user.is_authenticated:
        return redirect('instrutor_dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('instrutor_dashboard' if user.role == 'instrutor' else 'aluno_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('login')

