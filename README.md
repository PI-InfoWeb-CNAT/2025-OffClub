# Projeto OffClub 

**OffClub** é um projeto modelo (blueprint) para a disciplina de Análise e Projeto Orientado a Objetos — uma plataforma de ofertas e cupons desenvolvida em **Django** para fins educacionais e de demonstração.

---

## Visão Geral

- Linguagem: **Python (Django)**
- Estrutura do projeto: código-fonte em `src/`
- Banco de dados padrão: **SQLite** (`src/db.sqlite3`) para desenvolvimento
- Licença: **GPL-3.0**

---

## Contato / Equipe

- **Fellipe Aleixo** (orientador) - fellipe@ifrn.edu.br
- **Clara Teodósio** - clara.teodosio@escolar.ifrn.edu.br
- **Lucas Cássio** - lucas.cassio@escolar.ifrn.edu.br
- **Ermesson Andrade** - ermesson.a@escolar.ifrn.edu.br
- **Amanda Lara** - lara.amanda@escolar.ifrn.edu.br
- **Heitor Barboza** - franca.heitor@escolar.ifrn.edu.br

Canal de comunicação: **Discord** — https://discord.gg/929jPg67vD

---

## Setup (Windows PowerShell)

1. Clone o repositório:

```powershell
git clone <repo-url>
cd 2025-OffClub/src
```

2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale dependências:

```powershell
pip install -r requirements.txt
```

4. Rode migrações e crie o superusuário (ou use script):

```powershell
python manage.py migrate
python manage.py createsuperuser
# ou
python ..\scripts\create_superuser.py
```

5. (Opcional) Popule dados de exemplo:

```powershell
python ..\scripts\seed_data.py
```

6. Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

> Acesse em: http://127.0.0.1:8000

---

## Estrutura de alto nível

- `src/` – Código-fonte do projeto Django
  - `apps/` – Aplicações Django (cada domínio do sistema)
  - `config/` – Configurações do Django (base/dev/prod)
  - `scripts/` – Scripts utilitários (setup, seed, create_superuser)
  - `static/` e `templates/` – Recursos e templates globais
  - `manage.py` – CLI do Django
- `docs/` – Documentação do projeto (visão, casos de uso, modelo de domínio)

---

## Artefatos

- Visão do projeto: `docs/Visao_OffClub.md`
- Casos de uso: `docs/casos_de_uso/`
- Modelo ER e domínio: `docs/er/`, `docs/modelos_de_dominio/`
- [Mapa do site](https://www.figma.com/board/vEwdHDyp7MIktbrJIxaFMm/Mapa-do-site-Offclub?node-id=0-1&t=ewSuifi2DYR5T6vo-1)
* [Protótipo](https://www.figma.com/design/gKuAlxfR0AhlUVnhSf7Dfr/OffClub---Prot%C3%B3tipo---Designs?node-id=12-2&t=CWYd28mcVz5GG3T8-1)

