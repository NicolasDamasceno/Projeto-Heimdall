# Heimdall — Software de Controle de Acesso

Sistema web de controle de acesso desenvolvido como **Projeto Integrador** no curso de **Técnico em Desenvolvimento de Sistemas** do **IFPI Campus Teresina Central**, com o objetivo de aumentar a segurança institucional por meio da identificação digital de alunos, docentes e visitantes.

> *"Heimdall"* é uma referência ao deus nórdico guardião da ponte Bifrost — aquele que vigia e controla quem pode passar.

---

## 👥 Colaboradores

| Nome | Responsabilidades |
|------|-------------------|
| **Nicolas Antônio Damasceno Sales Campos** | Diagrama de Caso de Uso, Modelo Canva, MockUp, Design do Front-End, Telas de Alta Fidelidade, Back-End, Banco de Dados e Relatório |
| **Lyan Kaleu Meneses de Sousa** | Modelo DER, Modelo Lógico, Diagrama de Classes, Cronograma, Back-End (autorização, validação, views), Front-End e Banco de Dados |

**Orientador:** Prof. Dr. Adalton de Sena Almeida

---

## Sobre o Projeto

O Heimdall surgiu da necessidade identificada no próprio IFPI: alunos frequentemente acessavam a instituição sem apresentar identificação ao porteiro. A solução desenvolvida permite que a equipe de segurança verifique, em tempo real, se uma pessoa está cadastrada no sistema — através de busca por **nome**, **CPF** ou **matrícula** — e registra automaticamente cada entrada com data e horário.

O sistema também prevê situações em que o aluno não possui celular, carteirinha ou acesso à internet, permitindo a identificação apenas pela digitação da matrícula ou CPF.

---

## 🗂️ Estrutura do Projeto

```
Heimdall/
├── Heimdall/               # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── pages/                  # App principal
│   ├── models.py           # Modelos: Usuario, Aluno, Docente, Visitante, Entrada, Dispositivo
│   ├── views.py            # Views e lógica de negócio
│   ├── forms.py            # Formulários Django
│   ├── urls.py             # Rotas da aplicação
│   ├── admin.py            # Painel administrativo
│   ├── templates/
│   │   └── pages/
│   │       ├── index.html              # Dashboard principal
│   │       ├── validar_entrada.html    # Tela de validação de acesso
│   │       ├── listar_entradas.html    # Histórico de entradas
│   │       ├── cadastrar_visitante.html
│   │       ├── login.html
│   │       ├── register_admin.html
│   │       └── change_password.html
│   └── static/css/
│       └── styles.css
├── manage.py
└── requirements.txt
```

---

## Arquitetura e Conceitos Aplicados

### Herança com Polimorfismo (django-polymorphic)

O modelo central do sistema é `Usuario`, que herda de `PolymorphicModel` da biblioteca **django-polymorphic**. As subclasses `Aluno`, `Docente` e `Visitante` estendem essa classe base com atributos específicos:

```python
# models.py
class Usuario(PolymorphicModel):
    nome     = CharField(...)
    cpf      = CharField(unique=True)
    email    = EmailField(unique=True)
    tipo_usuario = CharField(choices=[ALUNO, DOCENTE, VISITANTE])

class Aluno(Usuario):           # herda de Usuario
    matricula          = CharField(unique=True)
    curso              = ForeignKey(Curso)
    situacao_matricula = CharField(choices=['Deferida', 'Indeferida'])

class Docente(Usuario):         # herda de Usuario
    departamento = CharField(...)

class Visitante(Usuario):       # herda de Usuario
    motivo_visita = CharField(...)
```

Graças ao polimorfismo, o sistema consegue buscar qualquer tipo de usuário com uma única query:

```python
# views.py — busca por CPF ou matrícula, independente do tipo
usuario = Usuario.objects.filter(cpf=cpf_ou_matricula).first()
if not usuario:
    usuario = Usuario.objects.filter(aluno__matricula=cpf_ou_matricula).first()
```

### Encapsulamento e Validação

A validação de CPF é encapsulada diretamente no modelo `Usuario`, usando a biblioteca **validate-docbr**, garantindo que dados inválidos nunca cheguem ao banco:

```python
def clean(self):
    cpf_validator = CPF()
    if not cpf_validator.validate(str(self.cpf)):
        raise ValidationError({'cpf': 'CPF inválido'})
```

A validação de matrícula (15 dígitos) também é encapsulada em `Aluno.clean()`, seguindo o mesmo princípio.

### Associação entre Modelos (ForeignKey)

Os modelos se relacionam por meio de chaves estrangeiras, refletindo a modelagem do banco de dados:

```
Entrada  →  Usuario    (quem entrou)
Entrada  →  Dispositivo (por qual catraca/computador)
Aluno    →  Curso       (em qual curso está matriculado)
```

### Class-Based View (CBV)

A tela principal utiliza uma **Class-Based View** com `TemplateView`, separando os métodos `GET` (exibição do dashboard) e `POST` (cadastro via formulário modal):

```python
class PaginaInicial(TemplateView):
    template_name = 'pages/index.html'

    def get(self, request, ...):   # exibe dashboard com totalizadores
        ...
    def post(self, request, ...):  # processa cadastro de alunos/docentes
        ...
```

### Autenticação e Controle de Acesso

O sistema usa o sistema de autenticação nativo do Django (`django.contrib.auth`), com acesso restrito apenas a usuários `is_staff`. O decorator `@login_required` protege rotas sensíveis como histórico e exportação.

---

## Funcionalidades

| Rota | Funcionalidade |
|------|---------------|
| `/` | Dashboard com totalizadores (alunos, docentes, visitantes, entradas do dia) e formulários de cadastro |
| `/validar-entrada/` | Validação de acesso por CPF ou matrícula; registra entrada com data/hora e dispositivo |
| `/listar-entradas/` | Histórico de entradas com filtros por nome, matrícula, dispositivo, tipo de usuário e período |
| `/exportar-csv/` | Exportação das entradas do dia em arquivo `.csv` |
| `/cadastrar-visitante/` | Cadastro de visitante e registro automático de entrada |
| `/excluir-entrada/<id>/` | Exclusão de um registro de entrada |
| `/login/` | Autenticação de administradores |
| `/register-admin/` | Cadastro do primeiro administrador do sistema |
| `/change-password/` | Alteração de senha |
| `/logout/` | Encerramento de sessão |

---

## Tecnologias Utilizadas

**Back-End**
- [Python 3](https://www.python.org/) + [Django 5.1.4](https://www.djangoproject.com/)
- [django-polymorphic 3.1.0](https://django-polymorphic.readthedocs.io/) — herança polimórfica nos modelos
- [validate-docbr 1.10.0](https://pypi.org/project/validate-docbr/) — validação de CPF
- [djangorestframework 3.15.2](https://www.django-rest-framework.org/) — base para API REST
- [drf-spectacular 0.28.0](https://drf-spectacular.readthedocs.io/) — documentação automática da API (Swagger)
- [pytz 2024.2](https://pypi.org/project/pytz/) — fuso horário (America/Fortaleza)

**Front-End**
- HTML5 + CSS3
- Interface responsiva com modais para feedback em tempo real

**Banco de Dados**
- SQLite3 (desenvolvimento)

---

## Modelo de Dados

```
USUARIO (base polimórfica)
├── id_usuario (PK)
├── cpf (único)
├── nome
├── email (único)
└── tipo_usuario (AL / DC / VT)
    ├── ALUNO → matricula (único), curso (FK), situacao_matricula
    ├── DOCENTE → departamento
    └── VISITANTE → motivo_visita

CURSO
├── id (PK)
├── nome
└── turno (manhã / tarde / noite)

DISPOSITIVO
├── id_dispositivo (PK)
├── localizacao
└── tipo_dispositivo (PC / CT)

ENTRADA
├── id_entrada (PK)
├── id_usuario (FK → USUARIO)
├── dispositivo (FK → DISPOSITIVO)
└── data_entrada (auto)
```

---

## ▶️ Como Executar

**Pré-requisitos:** Python 3.10+ instalado.

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd Heimdall

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (ou usar o /register-admin/ na primeira execução)
python manage.py createsuperuser

# Executar o servidor
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📄 Documentação

O relatório completo do projeto integrador, contendo problemática, metodologia, diagrama de classes, modelo DER, modelo lógico e diagrama de caso de uso, está disponível na pasta `/docs` do repositório.

---

## Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django-Polymorphic Documentation](https://django-polymorphic.readthedocs.io/)
- [Validate-docbr Documentation](https://pypi.org/project/validate-docbr/)
- [Python Official Documentation](https://docs.python.org/)
- Bhargava, A. Y. (2017). *Entendendo Algoritmos: Um Guia Ilustrado Para Programadores e Outros Curiosos.*

---

> Projeto Integrador — Técnico em Desenvolvimento de Sistemas  
> IFPI Campus Teresina Central · 2025
