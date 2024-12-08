from django.shortcuts import render, redirect
from .forms import FreteForm, MotoristaForm, CartaoForm, PagamentoForm, RegistroFiscalForm, TipoForm, VeiculoForm
from .models import Acessa, Carga, Motorista, Cartao, Frete, Fiscal, Pagamento, Tipo, Veiculo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

@login_required
def index(request):
    """A pagina inicial dos fiscais"""
    return render(request, 'gerenciamento/base/index.html')

@staff_member_required
def indexadmin(request):
    """A pagina inicial do administrador"""
    return render(request, 'gerenciamento/base/indexadmin.html')

@login_required
def cadastrarm(request):
    if request.method != 'POST':
        form = MotoristaForm()
    else:
        form = MotoristaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}
    return render(request, 'gerenciamento/motorista/cadastrarm.html', context)

@login_required
def sucesso(request):
    return render(request, 'gerenciamento/base/sucesso.html')

@login_required
def pesquisarm(request):
    motoristas = Motorista.objects.all().order_by('nome')
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/motorista/pesquisarm.html', context)

@login_required
def editarm(request):
    motoristas = Motorista.objects.all().order_by('nome')
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/motorista/editarm.html', context)

@login_required
def formeditarm(request, cpf_motorista):
    motoristas = Motorista.objects.get(cpf_motorista=cpf_motorista)
    
    form = MotoristaForm(request.POST or None,instance=motoristas)
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'motoristas': motoristas}
    return render(request, 'gerenciamento/motorista/formeditarm.html', context)

@login_required
def excluirm(request):
    motoristas = Motorista.objects.all().order_by('nome')
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/motorista/excluirm.html', context)

@login_required
def formexcluirm(request,cpf_motorista):

    motoristas = Motorista.objects.get(cpf_motorista=cpf_motorista)
    
    Cartao.objects.filter(cpf_motorista=cpf_motorista).update(cpf_motorista=None)
    
    Frete.objects.filter(cpf_motorista=cpf_motorista).update(cpf_motorista=None)

    motoristas.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')
    
@staff_member_required
def cadastraru(request):
    if request.method != 'POST':
        form = RegistroFiscalForm()
    else:
        form = RegistroFiscalForm(request.POST)
        if form.is_valid():
            # Create the user but don't save to the database yet
            user = form.save(commit=False)
            # Set the hashed password and save the user
            user.set_password(form.cleaned_data['password'])
            
            user.is_active = True
            user.is_admin = False
            
            user.save()
            return redirect('gerenciamento:sucesso')

    return render(request, 'gerenciamento/usuario/cadastraru.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        nome_usuario = request.POST.get('nome_usuario')
        password = request.POST.get('password')

        user = authenticate(request, nome_usuario=nome_usuario, password=password)

        if user is not None:
            login(request, user)
            user.last_login = timezone.now()  # Update last_login
            user.save()  # Save the user to update the last_login
            
            if user.is_staff:
                return redirect('gerenciamento:indexadmin')  # Redirect to homepage after login
            else:
                return redirect('gerenciamento:index')  # Redirect to homepage after login
            
            
        else:
            messages.error(request, "Nome de usuario ou senha inválidos, Tente novamente.")  # Update message to reflect changes

    return render(request, 'gerenciamento/login/login.html')

def logout_view(request):
    logout(request)
    return redirect('gerenciamento:login')  # Redirect to the login page after logging out

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'gerenciamento/login/password_reset.html'
    email_template_name = 'gerenciamento/login/password_reset_email.html'
    subject_template_name = 'gerenciamento/login/password_reset_subject.txt'
    success_message = "Um email foi enviado com as intruções para a redefinição da sua senha, " \
    "se uma conta com o email enviado existir você deve recebe-lo." \
    " Se ainda não o recebeu confirme o email digitado e verifique a caixa de spam." 
    success_url = reverse_lazy('gerenciamento:login')
    
def custom_password_reset_confirm(request, email):

    user = Fiscal.objects.get(email=email)
    
    form = RegistroFiscalForm(request.POST or None,instance=user)

    if form.is_valid():
        # Create the user but don't save to the database yet
        user = form.save(commit=False)
        # Set the hashed password and save the user
        user.set_password(form.cleaned_data['password'])
        
        user.is_active = True
        user.is_admin = False
        user.save()
        return redirect('gerenciamento:password_reset_complete')  

    context = {'form': form, 'user': user}
    
    return render(request, 'gerenciamento/login/editarsenha.html', context)

@login_required
def cadastrarc(request):
    if request.method != 'POST':
        form = CartaoForm()
        form.fields['cpf_motorista'].queryset = Motorista.objects.all()
        form.fields['cpf_motorista'].label_from_instance = lambda obj: f"{obj.cpf_motorista} - {obj.nome}"
    else:
        form = CartaoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}

    return render(request, 'gerenciamento/cartao/cadastrarc.html', context)

@login_required
def pesquisarc(request):
    cartoes = Cartao.objects.select_related('cpf_motorista').all().order_by('cpf_motorista')
    
    context = {
        'cartoes': cartoes
    }
    return render(request, 'gerenciamento/cartao/pesquisarc.html', context)

@login_required
def editarc(request):
    cartoes = Cartao.objects.select_related('cpf_motorista').all().order_by('cpf_motorista')
    
    context = {
        'cartoes': cartoes
    }
    return render(request, 'gerenciamento/cartao/editarc.html', context)

@login_required
def formeditarc(request, numero_conta):
    cartoes = Cartao.objects.get(numero_conta=numero_conta)
    
    form = CartaoForm(request.POST or None,instance=cartoes)
    form.fields['cpf_motorista'].queryset = Motorista.objects.all()
    form.fields['cpf_motorista'].label_from_instance = lambda obj: f"{obj.cpf_motorista} - {obj.nome}"
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'cartoes': cartoes}
    return render(request, 'gerenciamento/cartao/formeditarc.html', context)

@login_required
def excluirc(request):
    cartoes = Cartao.objects.select_related('cpf_motorista').all().order_by('cpf_motorista')
    
    context = {
        'cartoes': cartoes
    }
    return render(request, 'gerenciamento/cartao/excluirc.html', context)

@login_required
def formexcluirc(request,numero_conta):
    cartao = Cartao.objects.get(numero_conta=numero_conta)
    
    cartao.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')

@staff_member_required
def pesquisaru(request):
    usuarios = Fiscal.objects.all().order_by('nome_usuario')
    
    context = {
        'usuarios': usuarios
    }
    return render(request, 'gerenciamento/usuario/pesquisaru.html', context)

@staff_member_required
def editaru(request):
    usuarios = Fiscal.objects.all().order_by('nome_usuario')
    
    context = {
        'usuarios': usuarios
    }
    
    return render(request, 'gerenciamento/usuario/editaru.html', context)

@staff_member_required
def formeditaru(request, cpf_fiscal):
    usuario = Fiscal.objects.get(cpf_fiscal=cpf_fiscal)
    
    if request.method == 'POST':
        form = RegistroFiscalForm(data=request.POST, instance=usuario)
        form.fields.pop('password', None)
        form.fields.pop('password_confirm', None)
        
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')
    else:
        form = RegistroFiscalForm(instance=usuario)
        form.fields.pop('password', None)
        form.fields.pop('password_confirm', None)

    context = {'form': form, 'usuario': usuario}
    return render(request, 'gerenciamento/usuario/formeditaru.html', context)

@staff_member_required
def excluiru(request):
    usuarios = Fiscal.objects.all().order_by('nome_usuario')
    
    context = {
        'usuarios': usuarios
    }
    return render(request, 'gerenciamento/usuario/excluiru.html', context)

@staff_member_required
def formexcluiru(request, cpf_fiscal):
    usuario = Fiscal.objects.get(cpf_fiscal=cpf_fiscal)
    
    Pagamento.objects.filter(cpf_fiscal=cpf_fiscal).update(cpf_fiscal=None)
    
    Acessa.objects.filter(cpf_fiscal=cpf_fiscal).update(cpf_fiscal=None)
    
    usuario.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')

@login_required
def cadastrart(request):
    if request.method != 'POST':
        form = TipoForm()
    else:
        form = TipoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}

    return render(request, 'gerenciamento/tipo/cadastrart.html', context)

@login_required
def pesquisart(request):
    tipos = Tipo.objects.all().order_by('id_tipo')
    
    context = {
        'tipos': tipos
    }
    return render(request, 'gerenciamento/tipo/pesquisart.html', context)

@login_required
def editart(request):
    tipos = Tipo.objects.all().order_by('id_tipo')
    
    context = {
        'tipos': tipos
    }
    return render(request, 'gerenciamento/tipo/editart.html', context)

@login_required
def formeditart(request, id_tipo):
    
    tipo = Tipo.objects.get(id_tipo=id_tipo)
    
    form = TipoForm(request.POST or None,instance=tipo)
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'tipo': tipo}
    return render(request, 'gerenciamento/tipo/formeditart.html', context)

@login_required
def excluirt(request):
    tipos = Tipo.objects.all().order_by('id_tipo')
    
    context = {
        'tipos': tipos
    }
    return render(request, 'gerenciamento/tipo/excluirt.html', context)

@login_required
def formexcluirt(request, id_tipo):
    tipo = Tipo.objects.get(id_tipo=id_tipo)
    
    tipo.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')

@login_required
def cadastrarv(request):
    if request.method != 'POST':
        form = VeiculoForm()
        form.fields['id_tipo'].queryset = Tipo.objects.all()
        form.fields['id_tipo'].label_from_instance = lambda obj: f"{obj.id_tipo} - {obj.nome_tipo}"
    else:
        form = VeiculoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}

    return render(request, 'gerenciamento/veiculo/cadastrarv.html', context)

@login_required
def pesquisarv(request):
    veiculos = Veiculo.objects.select_related('id_tipo').all().order_by('modelo')
    
    context = {
        'veiculos': veiculos
    }
    return render(request, 'gerenciamento/veiculo/pesquisarv.html', context)

@login_required
def editarv(request):
    veiculos = Veiculo.objects.all().order_by('modelo')
    
    context = {
        'veiculos': veiculos
    }
    return render(request, 'gerenciamento/veiculo/editarv.html', context)

@login_required
def formeditarv(request, renavam):
    
    veiculo = Veiculo.objects.get(renavam=renavam)
    
    form = VeiculoForm(request.POST or None,instance=veiculo)
    form.fields['id_tipo'].queryset = Tipo.objects.all()
    form.fields['id_tipo'].label_from_instance = lambda obj: f"{obj.id_tipo} - {obj.nome_tipo}"
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'veiculo': veiculo}
    return render(request, 'gerenciamento/veiculo/formeditarv.html', context)

@login_required
def excluirv(request):
    veiculos = Veiculo.objects.all().order_by('modelo')
    
    context = {
        'veiculos': veiculos
    }
    return render(request, 'gerenciamento/veiculo/excluirv.html', context)

@login_required
def formexcluirv(request, renavam):
    veiculo = Veiculo.objects.get(renavam=renavam)
    
    Frete.objects.filter(renavam=renavam).update(renavam=None)
    
    veiculo.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')

@login_required
def cadastrarf(request):
    if request.method != 'POST':
        form = FreteForm()
        form.fields['cpf_motorista'].queryset = Motorista.objects.all()
        form.fields['cpf_motorista'].label_from_instance = lambda obj: f"{obj.cpf_motorista} - {obj.nome}"
        
        form.fields['renavam'].queryset = Veiculo.objects.all()
        form.fields['renavam'].label_from_instance = lambda obj: f"{obj.renavam} - {obj.modelo}"
    else:
        form = FreteForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}

    return render(request, 'gerenciamento/frete/cadastrarf.html', context)

@login_required
def pesquisarf(request):
    fretes = Frete.objects.select_related('renavam').all().order_by('id_frete') & Frete.objects.select_related('cpf_motorista').all().order_by('id_frete')
    
    context = {
        'fretes': fretes
    }
    return render(request, 'gerenciamento/frete/pesquisarf.html', context)

@login_required
def editarf(request):
    fretes = Frete.objects.select_related('cpf_motorista').all().order_by('id_frete')
    
    context = {
        'fretes': fretes
    }
    return render(request, 'gerenciamento/frete/editarf.html', context)

@login_required
def formeditarf(request, id_frete):
    
    frete = Frete.objects.get(id_frete=id_frete)
    
    form = FreteForm(request.POST or None,instance=frete)
    form.fields['cpf_motorista'].queryset = Motorista.objects.all()
    form.fields['cpf_motorista'].label_from_instance = lambda obj: f"{obj.cpf_motorista} - {obj.nome}"
        
    form.fields['renavam'].queryset = Veiculo.objects.all()
    form.fields['renavam'].label_from_instance = lambda obj: f"{obj.renavam} - {obj.modelo}"
    
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'frete': frete}
    return render(request, 'gerenciamento/frete/formeditarf.html', context)

@login_required
def excluirf(request):
    fretes = Frete.objects.select_related('cpf_motorista').all().order_by('id_frete')
    
    context = {
        'fretes': fretes
    }
    return render(request, 'gerenciamento/frete/excluirf.html', context)

@login_required
def formexcluirf(request, id_frete):
    frete = Frete.objects.get(id_frete=id_frete)
    
    Pagamento.objects.filter(id_frete=id_frete).update(id_frete=None)
    
    Carga.objects.filter(id_frete=id_frete).update(id_frete=None)
    
    frete.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')

@login_required
def cadastrarp(request):
    if request.method != 'POST':
        form = PagamentoForm()
        form.fields['cpf_fiscal'].queryset = Fiscal.objects.all()
        form.fields['cpf_fiscal'].label_from_instance = lambda obj: f"{obj.cpf_fiscal} - {obj.nome_usuario}"
        
        form.fields['id_frete'].queryset = Frete.objects.select_related('cpf_motorista').all()
        form.fields['id_frete'].label_from_instance = lambda obj: f"{obj.id_frete} - {obj.cpf_motorista.nome} - {obj.renavam}"
        
    else:
        form = PagamentoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}

    return render(request, 'gerenciamento/pagamento/cadastrarp.html', context)

@login_required
def pesquisarp(request):
    pagamentos = Pagamento.objects.select_related('cpf_fiscal').all().order_by('data_pagamento') & Pagamento.objects.select_related('id_frete').all().order_by('data_pagamento')
    
    context = {
        'pagamentos': pagamentos
    }
    
    return render(request, 'gerenciamento/pagamento/pesquisarp.html', context)

@login_required
def editarp(request):
    pagamentos = Pagamento.objects.select_related('cpf_fiscal').all().order_by('data_pagamento') & Pagamento.objects.select_related('id_frete').all().order_by('data_pagamento')
    
    context = {
        'pagamentos': pagamentos
    }
    return render(request, 'gerenciamento/pagamento/editarp.html', context)

@login_required
def formeditarp(request, id_pagamento):
    
    pagamento = Pagamento.objects.get(id_pagamento=id_pagamento)
    
    form = PagamentoForm(request.POST or None,instance=pagamento)
    form.fields['cpf_fiscal'].queryset = Fiscal.objects.all()
    form.fields['cpf_fiscal'].label_from_instance = lambda obj: f"{obj.cpf_fiscal} - {obj.nome_usuario}"
        
    form.fields['id_frete'].queryset = Frete.objects.select_related('cpf_motorista').all()
    form.fields['id_frete'].label_from_instance = lambda obj: f"{obj.id_frete} - {obj.cpf_motorista.nome} - {obj.renavam}"
    
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'pagamento': pagamento}
    return render(request, 'gerenciamento/pagamento/formeditarp.html', context)

@login_required
def excluirp(request):
    pagamentos = Pagamento.objects.select_related('cpf_fiscal').all().order_by('data_pagamento') & Pagamento.objects.select_related('id_frete').all().order_by('data_pagamento')
    
    context = {
        'pagamentos': pagamentos
    }
    return render(request, 'gerenciamento/pagamento/excluirp.html', context)

@login_required
def formexcluirp(request, id_pagamento):
    pagamento = Pagamento.objects.get(id_pagamento=id_pagamento)
    
    pagamento.delete()
    
    return render(request,'gerenciamento/base/sucesso.html')