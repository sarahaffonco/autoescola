# AutoEscola - Sistema de Gestão para Auto Escola

Sistema de gestão completo para auto escola, desenvolvido em Python com Django.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.12 + Django 5.0
- **Frontend**: HTML5 + Tailwind CSS 3.0
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Django Auth System

## 📋 Funcionalidades

### Para Instrutores
- Dashboard com métricas e estatísticas
- Visualização de aulas agendadas
- Acompanhamento de desempenho semanal
- Taxa de aprovação de alunos
- Gestão de aulas (agendadas, em andamento, completadas)

### Para Alunos
- Dashboard personalizado
- Acompanhamento de progresso (horas completadas)
- Visualização de próximas aulas
- Histórico de aulas realizadas
- Sistema de agendamento de aulas
- Acompanhamento de habilidades práticas

### Para Funcionários
- Acesso administrativo via Django Admin
- Gestão de usuários
- Gestão de aulas e agendamentos

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/meandrad/auto-drive-hub.git
cd auto-drive-hub
```

2. **Crie e ative um ambiente virtual**
```bash
python3 -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações do banco de dados**
```bash
python manage.py migrate
```

5. **Crie um superusuário (admin)**
```bash
python manage.py createsuperuser
```

6. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

7. **Acesse o sistema**
- Aplicação: http://localhost:8000/
- Admin: http://localhost:8000/admin/

## 📁 Estrutura do Projeto

```
auto-drive-hub/
├── autoescola/          # Configurações do projeto Django
│   ├── settings.py      # Configurações principais
│   ├── urls.py          # URLs principais
│   └── wsgi.py          # WSGI para deploy
├── accounts/            # App de autenticação e usuários
│   ├── models.py        # Modelo de usuário customizado
│   ├── views.py         # Views de login/registro
│   └── forms.py         # Formulários de autenticação
├── core/                # App principal com dashboards
│   ├── views.py         # Views dos dashboards
│   └── urls.py          # URLs do core
├── lessons/             # App de gestão de aulas
│   ├── models.py        # Modelos de Aula e Progresso
│   ├── forms.py         # Formulários de agendamento
│   └── admin.py         # Configuração do admin
├── templates/           # Templates HTML
│   ├── base.html        # Template base
│   ├── accounts/        # Templates de autenticação
│   └── core/            # Templates dos dashboards
├── static/              # Arquivos estáticos (CSS, JS)
├── requirements.txt     # Dependências Python
└── manage.py            # Script de gerenciamento Django
```

## 🎨 Estilização

O projeto utiliza **Tailwind CSS** via CDN com configuração personalizada incluindo:
- Paleta de cores customizada baseada no design original
- Gradientes personalizados
- Animações suaves
- Sistema de componentes reutilizáveis
- Design responsivo mobile-first

## 👥 Tipos de Usuário

### Aluno
- Visualiza seu progresso
- Agenda aulas
- Acompanha habilidades

### Instrutor
- Visualiza dashboard com métricas
- Gerencia aulas
- Acompanha desempenho

### Funcionário
- Acesso administrativo completo
- Gestão de usuários e aulas

## 🔐 Autenticação

O sistema utiliza o sistema de autenticação nativo do Django com:
- Modelo de usuário customizado
- Sistema de roles (aluno, instrutor, funcionário)
- Páginas de login e registro personalizadas
- Proteção de rotas com `@login_required`

## 📊 Modelos de Dados

### User (Usuário)
- Campos: username, email, full_name, phone, role
- Roles: aluno, instrutor, funcionario

### Lesson (Aula)
- Campos: student, instructor, date, time, duration, location, vehicle_type, status, score
- Status: scheduled, in-progress, completed, cancelled

### StudentProgress (Progresso do Aluno)
- Campos: student, skill, progress
- Skills: baliza, estacionamento, direção em via, conversões, ladeira

## 🚀 Deploy

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=seu_dominio.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### Comandos para Deploy
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

## 📝 Referências

Este projeto foi migrado de uma aplicação React/TypeScript para Django, mantendo toda a funcionalidade e estilização originais. O design foi baseado no repositório de referência [sarahaffonco/transito](https://github.com/sarahaffonco/transito).

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 📞 Suporte

Para dúvidas ou suporte, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Django**

