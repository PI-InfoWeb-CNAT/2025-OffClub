## 1. Visão geral

Estrutura base para um projeto Django com scripts de app personalizado e diretórios já estruturados. 

## 2. Estrutura de diretórios

```plaintext
.
├── .scaffolds/               # Templates para scaffolding de apps
│   ├── custom_app/           # Exemplo de uma aplicação comum
│   │   ├── migrations/       # Migrações do banco de dados
│   │   │   └── __init__.py
│   │   ├── static/           # Arquivos estáticos específicos desta app
│   │   │   └── app_name.css  # Exemplo de arquivo CSS
│   │   ├── templates/        # Templates HTML específicos desta app
│   │   │   └── app_name.html # Exemplo de template HTML
│   │   ├── __init__.py
│   │   ├── admin.py          # Registro de modelos no admin do Django
│   │   ├── apps.py           # Configurações da aplicação
│   │   ├── models.py         # Modelos do banco de dados
│   │   ├── services.py       # Exemplo de módulo para lógica de negócio
│   │   ├── tests.py          # Testes unitários para a aplicação
│   │   ├── urls.py           # URLs específicas da aplicação
│   │   └── views.py          # Views da aplicação
│   ├── custom_rest_app/      # Exemplo de uma aplicação para APIs REST
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py    # Serializadores para APIs REST
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
├── apps/                     # Aplicações Django personalizadas do projeto
│   └── __init__.py
├── config/                   # Configurações globais do projeto
│   ├── __pycache__/
│   ├── settings/             # Configurações do Django
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── base.py           # Configurações base compartilhadas
│   │   ├── dev.py            # Configurações para ambiente de desenvolvimento
│   │   └── prod.py           # Configurações para ambiente de produção
│   ├── asgi.py               # Ponto de entrada ASGI
│   ├── urls.py               # URLs principais do projeto
│   └── wsgi.py               # Ponto de entrada WSGI
├── scripts/                  # Scripts utilitários
│   ├── setup.ps1             # Exemplo de script de setup (PowerShell)
│   └── startapp.ps1          # Exemplo de script para iniciar uma aplicação (PowerShell)
├── static/                   # Arquivos estáticos globais do projeto
│   ├── css/
│   └── js/
├── templates/                # Templates HTML globais do projeto
│   └── base.html             # Exemplo de template base
├── .gitignore                # Arquivos e diretórios a serem ignorados pelo Git
├── manage.py                 # Utilitário de linha de comando para tarefas administrativas do Django
├── README.md                 # Este arquivo
└── requirements.txt          # Dependências Python do projeto
```

## 3. Scripts

_Script_ | **START APP** :

```bash
cd apps
```

```bash
python ../manage.py startapp --template=../.scaffolds/custom_app/ <app_name>  
```

```bash
cd .. 
```

_Script_ | **SETUP** :

```bash	
python -m venv .venv
```

```bash
.venv/bin/activate
```

```bash
pip install -r requirements.txt
```