# 🚀 Guia Rápido - AutoEscola Django

## 🎯 O que foi feito?

Este repositório foi **completamente migrado** de uma aplicação React/TypeScript para **Python com Django**, mantendo **100% das funcionalidades e estilização**.

## 📋 Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

## ⚡ Início Rápido (5 minutos)

### 1. Clone o repositório
```bash
git clone https://github.com/meandrad/auto-drive-hub.git
cd auto-drive-hub
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
```bash
python manage.py migrate
```

### 4. Popule com dados de exemplo
```bash
python manage.py populate_sample_data
```

### 5. Inicie o servidor
```bash
python manage.py runserver
```

### 6. Acesse a aplicação
Abra seu navegador em: **http://localhost:8000/**

## 🔑 Credenciais de Teste

### Instrutor
- **Usuário**: `carlos_mendes`
- **Senha**: `senha123`
- **Funcionalidades**: Dashboard com métricas, aulas agendadas, desempenho semanal

### Alunos
- **Usuário**: `maria_silva` / **Senha**: `senha123`
- **Usuário**: `joao_santos` / **Senha**: `senha123`
- **Usuário**: `ana_costa` / **Senha**: `senha123`
- **Funcionalidades**: Progresso de horas, agendamento de aulas, histórico

## 📱 Funcionalidades Disponíveis

### Para Instrutores
✅ Dashboard com estatísticas em tempo real
✅ Visualização de aulas do dia
✅ Gráfico de desempenho semanal
✅ Taxa de aprovação
✅ Lista de alunos ativos
✅ Gestão de horários

### Para Alunos
✅ Acompanhamento de progresso (20h obrigatórias CONTRAN)
✅ Agendamento de aulas práticas
✅ Visualização de próximas aulas
✅ Histórico de aulas completadas
✅ Monitoramento de habilidades (baliza, estacionamento, etc.)
✅ Estatísticas pessoais

### Sistema de Agendamento
✅ Seleção de data e horário
✅ Escolha de instrutor disponível
✅ Seleção de tipo de veículo (A, B, D)
✅ Escolha de local de encontro

## 🎨 Interface

A interface mantém o design moderno original com:
- ✨ Cores vibrantes (azul, verde água, verde)
- 🎭 Gradientes suaves
- 📊 Gráficos visuais
- 📱 Design responsivo
- ⚡ Animações suaves

## 🛠️ Comandos Úteis

### Desenvolvimento
```bash
# Verificar se há problemas
python manage.py check

# Criar novo superusuário para admin
python manage.py createsuperuser

# Acessar shell Django
python manage.py shell

# Limpar dados de teste
python manage.py flush
```

### Produção
```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Executar com Gunicorn
pip install gunicorn
gunicorn autoescola.wsgi:application
```

## 📁 Estrutura do Projeto

```
auto-drive-hub/
├── autoescola/          # Configurações Django
├── accounts/            # Autenticação e usuários
├── core/                # Dashboards principais
├── lessons/             # Sistema de aulas
├── templates/           # Templates HTML
│   ├── base.html
│   ├── accounts/
│   └── core/
├── manage.py            # Script Django
├── requirements.txt     # Dependências Python
└── README.md           # Documentação completa
```

## 🔐 Painel Administrativo

Acesse o admin em: **http://localhost:8000/admin/**

Primeiro crie um superusuário:
```bash
python manage.py createsuperuser
```

No admin você pode:
- Gerenciar todos os usuários
- Criar/editar aulas
- Visualizar progresso dos alunos
- Modificar dados do sistema

## 🌐 Deploy

### Heroku
```bash
# Adicionar ao requirements.txt
echo "gunicorn" >> requirements.txt
echo "dj-database-url" >> requirements.txt
echo "psycopg2-binary" >> requirements.txt

# Criar Procfile
echo "web: gunicorn autoescola.wsgi" > Procfile

# Deploy
heroku create seu-app
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py populate_sample_data
```

### PythonAnywhere / DigitalOcean / AWS
Consulte a documentação oficial do Django para deployment:
https://docs.djangoproject.com/en/5.0/howto/deployment/

## 📚 Documentação Adicional

- **README.md** - Documentação completa do projeto
- **MIGRATION_COMPARISON.md** - Comparação React vs Django
- **test_app.sh** - Script de teste automático

## 🐛 Solução de Problemas

### Erro: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Erro: "no such table"
```bash
python manage.py migrate
```

### Erro: "Port 8000 is already in use"
```bash
# Use outra porta
python manage.py runserver 8001
```

### Sem dados para visualizar
```bash
python manage.py populate_sample_data
```

## 💡 Próximos Passos

1. ✅ Explorar os dashboards
2. ✅ Testar agendamento de aulas
3. ✅ Criar novos usuários
4. ✅ Personalizar no admin
5. ✅ Adicionar suas próprias funcionalidades

## 🤝 Suporte

Se tiver dúvidas:
1. Consulte o README.md completo
2. Verifique o MIGRATION_COMPARISON.md
3. Abra uma issue no GitHub

## 🎓 Tecnologias Utilizadas

- **Backend**: Django 5.0 + Python 3.12
- **Frontend**: Django Templates + Tailwind CSS
- **Database**: SQLite (desenvolvimento)
- **Auth**: Django Authentication System

---

**Desenvolvido com ❤️ usando Django**

**Migração de React para Django - Dezembro 2024**
