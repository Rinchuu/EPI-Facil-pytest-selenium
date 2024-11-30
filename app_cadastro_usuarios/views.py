from django.shortcuts import render, redirect
from .models import Usuario , Epis, Acao
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import AcaoForm  # Supondo que você tenha um formulário AcaoForm
from django.utils import timezone

# View para registrar uma ação
def registrar_acao(request):
    if request.method == 'POST':
        form = AcaoForm(request.POST)
        if form.is_valid():
            # Salva a ação e redireciona o usuário
            acao = form.save(commit=False)
            acao.data_acao = timezone.now()  # Define a data de criação da ação para o momento atual
            acao.save()
            messages.success(request, 'Ação registrada com sucesso!')
            return redirect('listar_acoes')  # Redireciona para uma página, ex: lista de ações
        else:
            messages.error(request, 'Erro ao registrar a ação. Verifique os dados inseridos.')
    else:
        form = AcaoForm()

    context = {
        'form': form,
    }

    return render(request, 'epis/registrar_acao.html', context)


def listar_acoes(request):
    # Consulta todas as ações da base de dados, ordenadas pela data (mais recentes primeiro)
    acoes = Acao.objects.all().order_by('-data_acao')  # Ajuste o nome do campo 'data_acao' se necessário

    # Defina o contexto a ser passado para o template
    context = {
        'acoes': acoes,
    }

    # Renderiza o template 'listar_acoes.html' com os dados de ações
    return render(request, 'epis/listar_acoes.html', context)

#------------------------------------------BUSCAR E VISUALIZAR USUARIO------------------------------------------
def cadastro(request):
    return render(request,'usuarios/cadastro.html')

def usuarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        nivel_usuario = request.POST.get('nivel_usuario')

        # Verificar se todos os campos estão preenchidos
        if nome and email and senha:
            # Verificar se já existe um usuário com o mesmo email
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "Usuário com este email já está cadastrado!")
                # Não avança para a próxima página; continua na página atual
                return render(request, 'usuarios/cadastro.html')
            else:
                # Caso o email não esteja cadastrado, criar o novo usuário

                novo_usuario = Usuario(nome=nome, email=email, senha=senha)
                novo_usuario.save()
                messages.success(request, "Usuário cadastrado com sucesso!")
                return redirect('usuarios')  # Redireciona para a página após o sucesso
        else:
            messages.error(request, "Todos os campos são obrigatórios!")
            # Se houver erro, renderiza a página de novo
            return render(request, 'usuarios/cadastro.html')

    # Recuperar todos os usuários do banco de dados
    usuarios = {
        'usuarios': Usuario.objects.all()
    }

    # Renderizar a página com a lista de usuários
    return render(request, 'usuarios/usuarios.html', usuarios)

def listar_usuarios(request):
    # Obtém o termo de busca da query string
    termo_busca = request.GET.get('busca', '').strip()  # Remove espaços em branco desnecessários

    # Filtra usuários com base no termo de busca
    if termo_busca:
        # Busca por nome ou email usando icontains (case insensitive)
        usuarios = Usuario.objects.filter(
            nome__icontains=termo_busca
        ) | Usuario.objects.filter(
            email__icontains=termo_busca
        )
    else:
        # Se não houver busca, retorna todos os usuários
        usuarios = Usuario.objects.all()

    # Renderiza o template correto, passando a lista de usuários e o termo de busca
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios, 'termo_busca': termo_busca})

#------------------------------------Login de usuario funcional-----------------------------------------------

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            # Tenta encontrar o usuário no banco de dados com o email e a senha fornecidos
            usuario = Usuario.objects.get(email=email, senha=senha)
            # Se o usuário for encontrado, autentica o usuário
            request.session['usuario_id'] = usuario.id_usuario  # Salva o ID do usuário na sessão
            messages.success(request, 'Login realizado com sucesso!')
            # Após autenticar o usuário, salve também o nome na sessão
            request.session['usuario_nome'] = usuario.nome
            return redirect('epis')  # Redireciona para a página inicial ou outra página
        except Usuario.DoesNotExist:
            # Se o usuário não for encontrado, exibe uma mensagem de erro
            messages.error(request, 'Email ou senha inválidos')

    return render(request, 'usuarios/login.html')


def logout_view(request):
    # Remove o ID do usuário da sessão, efetivamente fazendo logout
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')  # Redireciona para a página de login


#---------------------------------------------DELETAR USUARIO-------------------------------------------------
def deletar_usuario(request, id_usuario):
    # Busca o usuário pelo id ou retorna um erro 404 se não encontrar
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    
    # Deleta o usuário
    usuario.delete()

    # Redireciona de volta para a lista de usuários (ou outra página)
    return redirect('listar_usuarios')

#--------------------------------------------EDITAR USUARIO----------------------------------------------------
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)  # Use o mesmo nome do parâmetro da URL

    if request.method == 'POST':
        usuario.nome = request.POST['nome']
        usuario.email = request.POST['email']
        usuario.senha = request.POST['senha']
        usuario.nivel_usuario = request.POST['nivel_usuario']
        usuario.save()
        return redirect('listar_usuarios')  # Redireciona de volta para a lista de usuários

    return render(request, 'usuarios/editar.html', {'usuario': usuario})  # Renderiza o template de edição

#------------------------------------------BUSCAR E VISUALIZAR EPI------------------------------------------
def cadastro_epi(request):
    return render(request,'epis/cadastro_epi.html')

def epis(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        valor = request.POST.get('valor')

        # Verificar se todos os campos estão preenchidos
        if nome and quantidade and valor:
            # Verificar se já existe um usuário com o mesmo email
            if Epis.objects.filter(nome=nome).exists():
                messages.error(request, "Epi com esse nome já está cadastrado!")
                # Não avança para a próxima página; continua na página atual
                return render(request, 'epis/cadastro_epi.html')
            else:
                # Caso o email não esteja cadastrado, criar o novo usuário

                novo_epi = Epis(nome=nome, quantidade=quantidade, valor=valor)
                novo_epi.save()
                messages.success(request, "Epi cadastrado com sucesso!")
                return redirect('epis')  # Redireciona para a página após o sucesso
        else:
            messages.error(request, "Todos os campos são obrigatórios!")
            # Se houver erro, renderiza a página de novo
            return render(request, 'epis/cadastro_epi.html')

    # Recuperar todos os usuários do banco de dados
    epis = {
        'epis': Epis.objects.all()
    }

    # Renderizar a página com a lista de usuários
    return render(request, 'epis/epis.html', epis)

def listar_epis(request):
    # Obtém o termo de busca da query string
    termo_busca = request.GET.get('busca', '').strip()  # Remove espaços em branco desnecessários

    # Filtra usuários com base no termo de busca
    if termo_busca:
        # Busca por nome ou email usando icontains (case insensitive)
        epis = Epis.objects.filter(
            nome__icontains=termo_busca
        )
    else:
        # Se não houver busca, retorna todos os usuários
        epis = Epis.objects.all()

    # Renderiza o template correto, passando a lista de usuários e o termo de busca
    return render(request, 'epis/epis.html', {'epis': epis, 'termo_busca': termo_busca})

#--------------------------------------------EDITAR EPI----------------------------------------------------
def editar_epi(request, id_epi):
    epi = get_object_or_404(Epis, id_epi=id_epi)  # Use o mesmo nome do parâmetro da URL

    if request.method == 'POST':
        epi.nome = request.POST['nome']
        epi.quantidade = request.POST['quantidade']
        epi.valor = request.POST['valor']
        epi.save()
        return redirect('listar_epis')  # Redireciona de volta para a lista de usuários

    return render(request, 'epis/editar_epi.html', {'epi': epi})  # Renderiza o template de ediçãos

#---------------------------------------------DELETAR USUARIO-------------------------------------------------
def deletar_epi(request, id_epi):
    # Busca o usuário pelo id ou retorna um erro 404 se não encontrar
    epi = get_object_or_404(Epis, id_epi=id_epi)

    # Deleta o usuário
    epi.delete()

    # Redireciona de volta para a lista de usuários (ou outra página)
    return redirect('listar_epis')
