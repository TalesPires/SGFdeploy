from django import forms
from .models import Frete, Motorista, Cartao, Fiscal, Pagamento, Tipo, Veiculo
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNH, RENAVAM
import datetime
from django.utils.timezone import localtime


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['cpf_motorista','registro_cnh','nome', 'telefone','endereco', 'data_admissao']
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        
    def clean_cpf_motorista(self):
        cpf = self.cleaned_data.get('cpf_motorista')
        validator = CPF()

        if not validator.validate(cpf):
            raise ValidationError("CPF inválido.")
        
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        if len(telefone) != 11 or not telefone.isdigit():
            raise ValidationError("Telefone inválido. Deve conter 11 dígitos.")
        
        return telefone
    
    def clean_registro_cnh(self):
        cnh = self.cleaned_data.get('registro_cnh')
        validator = CNH()

        if not validator.validate(cnh):
            raise ValidationError("CNH inválido.")
        
        return cnh
    
class CartaoForm(forms.ModelForm):
    class Meta:
        model = Cartao
        fields = ['cpf_motorista','agencia', 'numero_conta', 'validade']
        widgets = {
            'validade': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        
class RegistroFiscalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = Fiscal
        fields = ['cpf_fiscal','nome_usuario','email', 'is_active', 'is_admin']
        
    def clean_cpf_fiscal(self):
        cpf = self.cleaned_data.get('cpf_fiscal')
        validator = CPF()

        if not validator.validate(cpf):
            raise ValidationError("CPF inválido.")
        
        return cpf
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("As senhas não correspondem")
        return cleaned_data
    
class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['id_tipo','nome_tipo', 'capacidade_peso', 'quantidade_eixos']
    
    def clean_capacidade_peso(self):
        capacidade_peso = self.cleaned_data.get('capacidade_peso')  # Use string key
        quantidade_eixos = self.cleaned_data.get('quantidade_eixos')  # Use string key
        
        if capacidade_peso is not None and capacidade_peso < 0:
            raise ValidationError('Capacidade de peso deve ser maior que zero')
        
        if quantidade_eixos is not None and quantidade_eixos < 0:
            raise ValidationError('Quantidade de eixos deve ser maior que zero')

        return capacidade_peso  # Ensure to return the cleaned value if valid

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['renavam','id_tipo', 'placa', 'marca','modelo', 'cor', 'rntrc', 'ano']
    
    ano = forms.CharField(
        max_length=4,
        widget=forms.TextInput(),
        label="Ano"
    )

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        if not ano.isdigit():
            raise forms.ValidationError("O ano deve ser um número.")
        if len(ano) != 4:
            raise forms.ValidationError("O ano deve ter 4 dígitos.")
        current_year = datetime.datetime.now().year
        if int(ano) > current_year + 1:
            raise forms.ValidationError(f"O ano não pode ser maior que o proximo ano ({current_year + 1 })")
        elif int(ano) < 1970:
            raise forms.ValidationError(f"O ano não pode ser meno que 1970")
        return ano

    def clean_renavam(self):
        renavam = self.cleaned_data.get('renavam')
        validator = RENAVAM()

        if not validator.validate(renavam):
            raise ValidationError("Renavam inválido.")
        
        return renavam
    
class FreteForm(forms.ModelForm):
    class Meta:
        model = Frete
        fields = ['id_frete','cpf_motorista','renavam','data_chegada','data_saida','distancia_rodagem','valor_frete']
        
        widgets = {
            'data_chegada': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  # HTML5 input type for DateTime
                    'class': 'form-control',  # Bootstrap class for styling
                }
            ),
            'data_saida': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  # HTML5 input type for DateTime
                    'class': 'form-control',  # Bootstrap class for styling
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format datetime fields for 'datetime-local' input
        if self.instance and self.instance.pk:  # Ensure it's an existing instance
            if self.instance.data_chegada:
                self.initial['data_chegada'] = localtime(self.instance.data_chegada).strftime('%Y-%m-%dT%H:%M')
            if self.instance.data_saida:
                self.initial['data_saida'] = localtime(self.instance.data_saida).strftime('%Y-%m-%dT%H:%M')
                
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['cpf_fiscal', 'id_frete', 'taxa_desconto', 'taxa_acrescimo', 'valor_calculado','data_pagamento', 'status_pagamento']
        widgets = {
            'status_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'data_pagamento': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',  
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format datetime fields for 'datetime-local' input
        if self.instance and self.instance.pk:  # Ensure it's an existing instance
            if self.instance.data_pagamento:
                self.initial['data_pagamento'] = localtime(self.instance.data_pagamento).strftime('%Y-%m-%dT%H:%M')