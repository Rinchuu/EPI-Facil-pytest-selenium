from django.urls import path
from django.contrib import admin
from app_cadastro_usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #rota, view responsavel,nome de referencia.
    #pagina inicial login
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #pagina de editar usuarios e deletar usuarios
    path('usuarios/deletar/<int:id_usuario>/', views.deletar_usuario, name='deletar_usuario'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    #paginas de caadastro e visualização de usuarios
    path('usuarios/cadastro/', views.cadastro, name='cadastro'),
    path('usuarios/cadastro/lista/', views.usuarios, name='usuarios'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    #paginas de cadastro/edit de epi
    path('epis/cadastro/', views.cadastro_epi, name='cadastro_epi'),
    path('epis/cadastro/lista/', views.epis, name='epis'),
    path('epis/editar/<int:id_epi>/', views.editar_epi, name='editar_epi'),
    path('epis/deletar/<int:id_epi>/', views.deletar_epi, name='deletar_epi'),
    path('epis/', views.listar_epis, name='listar_epis'),
    path('epis/registrar_acao/', views.registrar_acao, name='registrar_acao'),
    path('epis/listar_acoes/', views.listar_acoes, name='listar_acoes'),
]
