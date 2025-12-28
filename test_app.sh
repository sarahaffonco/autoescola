#!/bin/bash

# Script para testar a aplicação Django

echo "=========================================="
echo "   Teste da Aplicação AutoEscola Django  "
echo "=========================================="
echo ""

# Verificar se o Python está instalado
echo "1. Verificando Python..."
python3 --version
echo ""

# Verificar se as dependências estão instaladas
echo "2. Verificando dependências..."
pip3 list | grep Django
echo ""

# Executar verificações do Django
echo "3. Executando verificações do Django..."
python3 manage.py check
echo ""

# Verificar migrações
echo "4. Verificando migrações..."
python3 manage.py showmigrations
echo ""

# Criar superusuário (se não existir)
echo "5. Dados de teste disponíveis:"
echo "   - Instrutor: carlos_mendes / senha123"
echo "   - Aluno: maria_silva / senha123"
echo ""

# Instruções de uso
echo "=========================================="
echo "   Como executar a aplicação             "
echo "=========================================="
echo ""
echo "1. Ative o ambiente virtual (se houver):"
echo "   source venv/bin/activate"
echo ""
echo "2. Inicie o servidor:"
echo "   python3 manage.py runserver"
echo ""
echo "3. Acesse no navegador:"
echo "   http://localhost:8000/"
echo ""
echo "4. Para acessar o admin:"
echo "   http://localhost:8000/admin/"
echo "   (Crie um superusuário com: python3 manage.py createsuperuser)"
echo ""
echo "=========================================="
