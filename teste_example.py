from django.test import TestCase
import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.timezone import now
from django.contrib.auth.models import User
from app_cadastro_usuarios.models import Usuario, Epis, Acao

class ModelsTestCase(TestCase):

    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        # Criar um usuário
        self.usuario = Usuario.objects.create(
            nome="João Silva",
            email="joao.silva@example.com",
            senha="senha123",
            nivel_usuario="Cliente"
        )

        # Criar um equipamento (EPI)
        self.equipamento = Epis.objects.create(
            nome="Capacete de Segurança",
            quantidade="10",
            valor=50.00
        )

@pytest.mark.django_db
def test_cadastrar_usuario_sucesso(client):
    # Ação: Envia um POST com dados válidos
    response = client.post(reverse('usuarios'), {
        'nome': 'Novo Usuário',
        'email': 'novo@user.com',
        'senha': 'senha123',
        'nivel_usuario': '1'
    })

    # Verificação: Usuário foi criado e redirecionamento ocorreu
    assert response.status_code == 302
    assert Usuario.objects.filter(email='novo@user.com').exists()

@pytest.mark.django_db
def test_cadastrar_usuario_email_existente(client):
    # Configuração: Cria um usuário existente
    Usuario.objects.create(nome='Existente', email='existente@user.com', senha='senha123')

    # Ação: Tenta cadastrar um usuário com o mesmo email
    response = client.post(reverse('usuarios'), {
        'nome': 'Novo Usuário',
        'email': 'existente@user.com',
        'senha': 'senha456',
        'nivel_usuario': '1'
    })

    # Verificação: Cadastro falhou e mensagem foi exibida
    assert response.status_code == 200
    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "Usuário com este email já está cadastrado!" in messages


@pytest.mark.django_db
def test_cadastrar_epi_sucesso(client):
    # Ação: Envia um POST com dados válidos
    response = client.post(reverse('epis'), {
        'nome': 'Capacete',
        'quantidade': 10,
        'valor': 50.00
    })

    # Verificação: EPI foi criado e redirecionamento ocorreu
    assert response.status_code == 302
    assert Epis.objects.filter(nome='Capacete').exists()

@pytest.mark.django_db
def test_cadastrar_epi_nome_existente(client):
    # Configuração: Cria um EPI existente
    Epis.objects.create(nome='Capacete', quantidade=5, valor=40.00)

    # Ação: Tenta cadastrar um EPI com o mesmo nome
    response = client.post(reverse('epis'), {
        'nome': 'Capacete',
        'quantidade': 10,
        'valor': 50.00
    })

    # Verificação: Cadastro falhou e mensagem foi exibida
    assert response.status_code == 200
    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "Epi com esse nome já está cadastrado!" in messages


@pytest.mark.django_db
def test_logout_view(client):
    # Configuração: Simula um usuário autenticado na sessão
    session = client.session
    session['usuario_id'] = 1
    session.save()

    # Ação: Realiza o logout
    response = client.get(reverse('logout'))
    
    # Verificação: Sessão foi limpa e redirecionamento ocorreu
    assert 'usuario_id' not in client.session
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_listar_acoes(client):
    # Configuração: Cria dependências
    usuario = Usuario.objects.create(nome='Test User', email='test@example.com', senha='password')
    equipamento = Epis.objects.create(nome='Equipamento 1', quantidade='10', valor=100.00)

    # Configuração: Cria algumas ações
    Acao.objects.create(
        nome_equipamento=equipamento,
        usuario=usuario,
        data_emprestimo=now(),
        data_prevista_devolucao=now(),
        status='emprestado'
    )
    Acao.objects.create(
        nome_equipamento=equipamento,
        usuario=usuario,
        data_emprestimo=now(),
        data_prevista_devolucao=now(),
        status='devolvido'
    )

    # Ação: Faz a requisição GET
    response = client.get(reverse('listar_acoes'))

    # Verificação: As ações aparecem na resposta
    assert response.status_code == 200
    assert 'Equipamento 1' in response.content.decode()


@pytest.mark.django_db
def test_registrar_acao_sucesso(client):
    # Configuração: Cria um EPI e um Usuário
    equipamento = Epis.objects.create(nome='Capacete', quantidade=10, valor=50.00)
    assert equipamento.id_epi is not None  # Confirma que o EPI possui um ID

    usuario = Usuario.objects.create(nome='Test User', email='test@example.com', senha='password')
    assert usuario.id_usuario is not None  # Confirma que o usuário possui um ID

    # Ação: Envia um POST com dados válidos
    response = client.post(reverse('registrar_acao'), {
        'nome_equipamento': equipamento.id_epi,  # Use id_epi aqui
        'usuario': usuario.id_usuario,
        'data_emprestimo': now(),
        'data_prevista_devolucao': now(),
        'status': 'emprestado',
    })

    # Verificação: Ação foi registrada com sucesso
    assert response.status_code == 302
    assert Acao.objects.filter(nome_equipamento=equipamento, usuario=usuario, status='emprestado').exists()

@pytest.mark.django_db
def test_listar_acoes_autenticado(client):
    # Configuração: Cria e autentica um usuário
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

@pytest.mark.django_db
def test_login_view_valid_user(client):
    # Configuração: Cria um usuário
    Usuario.objects.create(email="test@test.com", senha="password123", nome="Teste User", id_usuario=1)
    
    # Ação: Envia um POST com email e senha válidos
    response = client.post(reverse('login'), {
        'email': 'test@test.com',
        'senha': 'password123',
    })
    
    # Verificação: O redirecionamento ocorreu e a sessão foi criada
    assert response.status_code == 302
    assert response.url == reverse('epis')
    assert client.session['usuario_id'] == 1

@pytest.mark.django_db
def test_login_view_invalid_user(client):
    # Ação: Envia um POST com credenciais inválidas
    response = client.post(reverse('login'), {
        'email': 'wrong@test.com',
        'senha': 'wrongpassword',
    })

    # Verificação: Login falhou e mensagem de erro foi gerada
    assert response.status_code == 200
    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert 'Email ou senha inválidos' in messages
