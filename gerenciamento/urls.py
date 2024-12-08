"""Define os URL patterns de gerenciamento."""

from django.urls import path
from . import views
from gerenciamento.views import ResetPasswordView
from django.contrib.auth import views as auth_views

app_name = 'gerenciamento'

urlpatterns = [
    # Pagina inicial
    path('', views.index, name='index'),
    # Pagina inicial admin
    path('iadmin/', views.indexadmin, name='indexadmin'),
    # Pagina de cadastro dos motoristas
    path('cadastrarm/', views.cadastrarm, name='cadastrarm'),
    # Pagina de sucesso
    path('sucesso/', views.sucesso, name='sucesso'),
    # Pagina de sucesso
    path('pesquisarm/', views.pesquisarm, name='pesquisarm'),
    # Pagina de edição dos motoristas
    path('editarm/', views.editarm, name='editarm'),
    # Pagina inserção dos dados da edição dos motoristas
    path('formeditarm/<str:cpf_motorista>/', views.formeditarm, name='formeditarm'),
    # Pagina de exclusão dos motoristas
    path('excluirm/', views.excluirm, name='excluirm'),
    # Pagina de exclusão dos motoristas
    path('excluirm/<str:cpf_motorista>/', views.formexcluirm, name='formexcluirm'),
    # Pagina de cadastro dos usuarios
    path('cadastraru/', views.cadastraru, name='cadastraru'),
    # Pagina de login
    path('login/', views.login_view, name='login'),
    # Pagina de logout
    path('logout/', views.logout_view, name='logout'),
    # Pagina de inserção do email para a redefinição de senha
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    # Pagina de redefinição da senha do usuario
    path('password-reset-confirm/<str:email>/', views.custom_password_reset_confirm, name='redefinir_senha'),
    # Pagina de sucesso da redefinação da senha
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='gerenciamento/login/password_reset_complete.html'),
    name='password_reset_complete'),
    # Pagina de cadastro dos cartões
    path('cadastrarc/', views.cadastrarc, name='cadastrarc'),
    # Pagina de pesquisa dos cartões
    path('pesquisarc/', views.pesquisarc, name='pesquisarc'),
    # Pagina de edição dos cartões
    path('editarc/', views.editarc, name='editarc'),
    # Pagina inserção dos dados da edição dos cartões
    path('formeditarc/<str:numero_conta>/', views.formeditarc, name='formeditarc'),
    # Pagina de exclusão dos cartões
    path('excluirc/', views.excluirc, name='excluirc'),
    # Pagina de exclusão dos cartões
    path('excluirc/<str:numero_conta>/', views.formexcluirc, name='formexcluirc'),
    # Pagina de pesquisa dos usuarios
    path('pesquisaru/', views.pesquisaru, name='pesquisaru'),
    # Pagina de edição dos usuarios
    path('editaru/', views.editaru, name='editaru'),
    # Pagina inserção dos dados da edição dos usuarios
    path('formeditaru/<str:cpf_fiscal>/', views.formeditaru, name='formeditaru'),
    # Pagina de exclusão dos usuarios
    path('excluiru/', views.excluiru, name='excluiru'),
    # Pagina de exclusão dos usuarios
    path('excluiru/<str:cpf_fiscal>/', views.formexcluiru, name='formexcluiru'),
    # Pagina de cadastro dos tipos de veículos
    path('cadastrart/', views.cadastrart, name='cadastrart'),
    # Pagina de pesquisa dos tipos de veículos
    path('pesquisart/', views.pesquisart, name='pesquisart'),
    # Pagina de edição dos tipos de veículos
    path('editart/', views.editart, name='editart'),
    # Pagina inserção dos dados da edição dos tipos de veículos
    path('formeditart/<str:id_tipo>/', views.formeditart, name='formeditart'),
    # Pagina de exclusão dos tipos de veículos
    path('excluirt/', views.excluirt, name='excluirt'),
    # Pagina de exclusão dos motoristas
    path('excluirt/<str:id_tipo>/', views.formexcluirt, name='formexcluirt'),
    # Pagina de cadastro dos veículos
    path('cadastrarv/', views.cadastrarv, name='cadastrarv'),
    # Pagina de pesquisa dos tipos de veículos
    path('pesquisarv/', views.pesquisarv, name='pesquisarv'),
    # Pagina de edição dos tipos de veículos
    path('editarv/', views.editarv, name='editarv'),
    # Pagina inserção dos dados da edição dos tipos de veículos
    path('formeditarv/<str:renavam>/', views.formeditarv, name='formeditarv'),
    # Pagina de exclusão dos tipos de veículos
    path('excluirv/', views.excluirv, name='excluirv'),
    # Pagina de exclusão dos motoristas
    path('excluirv/<str:renavam>/', views.formexcluirv, name='formexcluirv'),
    # Pagina de cadastro dos veículos
    path('cadastrarf/', views.cadastrarf, name='cadastrarf'),
    # Pagina de pesquisa dos tipos de veículos
    path('pesquisarf/', views.pesquisarf, name='pesquisarf'),
    # Pagina de edição dos tipos de veículos
    path('editarf/', views.editarf, name='editarf'),
    # Pagina inserção dos dados da edição dos tipos de veículos
    path('formeditarf/<str:id_frete>/', views.formeditarf, name='formeditarf'),
    # Pagina de exclusão dos tipos de veículos
    path('excluirf/', views.excluirf, name='excluirf'),
    # Pagina de exclusão dos motoristas
    path('excluirf/<str:id_frete>/', views.formexcluirf, name='formexcluirf'),
    # Pagina de cadastro dos veículos
    path('cadastrarp/', views.cadastrarp, name='cadastrarp'),
    # Pagina de pesquisa dos tipos de veículos
    path('pesquisarp/', views.pesquisarp, name='pesquisarp'),
    # Pagina de edição dos tipos de veículos
    path('editarp/', views.editarp, name='editarp'),
    # Pagina inserção dos dados da edição dos tipos de veículos
    path('formeditarp/<str:id_pagamento>/', views.formeditarp, name='formeditarp'),
    # Pagina de exclusão dos tipos de veículos
    path('excluirp/', views.excluirp, name='excluirp'),
    # Pagina de exclusão dos motoristas
    path('excluirp/<str:id_pagamento>/', views.formexcluirp, name='formexcluirp'),
]