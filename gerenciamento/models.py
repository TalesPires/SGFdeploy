from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class Motorista(models.Model):
    cpf_motorista = models.CharField(db_column='cpf_motorista',max_length=11,primary_key=True)
    registro_cnh = models.CharField(max_length=11)
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    data_admissao = models.DateField()

    class Meta:
        managed = False
        db_table = 'motorista'

    def __str__(self):
        return self.cpf_motorista

class Cartao(models.Model):
    agencia = models.CharField(max_length=5)
    cpf_motorista = models.ForeignKey(Motorista,db_column="cpf_motorista",on_delete=models.SET_DEFAULT,default="0")
    numero_conta = models.CharField(max_length=6,primary_key=True)
    validade = models.DateField()
    
    class Meta:
        managed = False
        db_table = 'cartao'

    def __str__(self):
        return self.numero_conta

class MinhaGestaoUsuarios(BaseUserManager):
    def criar_usuario(self, nome_usuario, email, cpf_fiscal, password=None):
        if not cpf_fiscal:
            raise ValueError("Por favor informe um CPF")
        
        if not nome_usuario:
            raise ValueError("Por favor informe um nome")
        
        if not email:
            raise ValueError("Por favor informe um email")
        
        # Create the user object with necessary fields
        user = self.model(
            email=self.normalize_email(email),
            nome_usuario=nome_usuario,
            cpf_fiscal=cpf_fiscal,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def criar_superuser(self, nome_usuario, email, cpf_fiscal, password=None):
        user = self.criar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            cpf_fiscal=cpf_fiscal,
            password=password
        )

        user.is_staff = True
        user.save(using=self._db)
        return user

class Fiscal(AbstractBaseUser):
    cpf_fiscal = models.CharField(primary_key=True, max_length=11)
    nome_usuario = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=55)
    is_active = models.BooleanField(db_column='ativo',default=True)     
    is_admin = models.BooleanField(db_column='staff',default=False) 

    objects = MinhaGestaoUsuarios()

    USERNAME_FIELD = 'nome_usuario'
    REQUIRED_FIELDS = ['email', 'cpf_fiscal']  

    class Meta:
        managed = False  
        db_table = 'fiscal'

    def __str__(self):
        return self.cpf_fiscal
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nome_tipo = models.CharField(max_length=20)
    capacidade_peso = models.DecimalField(decimal_places=2,max_digits=9)
    quantidade_eixos = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tipo'

    def __str__(self):
        return str(self.id_tipo)
    
class Veiculo(models.Model):
    renavam = models.CharField(max_length=11,primary_key=True)
    id_tipo = models.ForeignKey(Tipo,db_column='id_tipo',null=True,on_delete=models.SET_NULL)
    placa = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    cor = models.CharField(max_length=20)
    ano = models.CharField(max_length=4)
    rntrc = models.CharField(max_length=8)
    
    class Meta:
        managed = False
        db_table = 'veiculo'

    def __str__(self):
        return str(self.renavam)
    
class Frete(models.Model):
    id_frete = models.AutoField(primary_key=True)
    cpf_motorista = models.ForeignKey(Motorista,db_column='cpf_motorista',max_length=11, null=False,
    on_delete=models.SET_DEFAULT,blank=False,default="00000000000")  
    renavam = models.ForeignKey(Veiculo,db_column='renavam',max_length=11, null=False,
    on_delete=models.SET_DEFAULT,blank=False,default="00000000000")
    data_chegada = models.DateTimeField()
    data_saida = models.DateTimeField()
    distancia_rodagem = models.PositiveSmallIntegerField()
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'frete'

    def __str__(self):
        return str(self.id_frete)
    
class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    cpf_fiscal = models.ForeignKey(Fiscal,db_column='cpf_fiscal', max_length=11,on_delete=models.SET_DEFAULT,default="000", null=False,blank=False)
    id_frete = models.ForeignKey(Frete,db_column='id_frete',on_delete=models.SET_NULL,null=True)
    taxa_desconto = models.DecimalField(max_digits=8,decimal_places=2)
    taxa_acrescimo = models.DecimalField(max_digits=8,decimal_places=2)
    valor_calculado = models.DecimalField(max_digits=12,decimal_places=2)
    data_pagamento = models.DateTimeField()
    
    class escolhas_status_pagamento(models.TextChoices):
        PENDENTE = "PE",_("Pendente")
        EM_TRANSFERENCIA = "TR",_("Em Transferência")
        PAGO = "PA",_("Pago")

    status_pagamento = models.CharField(
        max_length=2,
        choices=escolhas_status_pagamento.choices,
        default=escolhas_status_pagamento.PENDENTE,
    )
    
    class Meta:
        managed = False
        db_table = 'pagamento'

    def __str__(self):
        return str(self.id_pagamento)
    
class Acessa(models.Model):
    cpf_fiscal = models.ForeignKey(Fiscal,db_column='cpf_fiscal',max_length=11,on_delete=models.SET_DEFAULT,default="000", null=False,blank=False)
    id_tipo = models.ForeignKey(Tipo,db_column='id_tipo'    ,null=True,on_delete=models.SET_NULL) 
    data_alteracao = models.DateTimeField(primary_key=True)
    valor_km = models.DecimalField(max_digits=9,decimal_places=2)
    valor_tonelada = models.DecimalField(max_digits=9,decimal_places=2)
    valor_entrega = models.DecimalField(max_digits=12,decimal_places=2)
    
    class Meta:
        managed = False
        db_table = 'acessa'

    def __str__(self):
        return self.id_tipo, self.cpf_fiscal, self.data_alteracao
    
class Carga(models.Model):
    codigo_carga = models.AutoField(primary_key=True)
    id_frete = models.ForeignKey(Frete,db_column='id_frete',null=True,on_delete=models.SET_NULL,blank=True)
    peso = models.DecimalField(max_digits=9, decimal_places=2)
    valor_carga = models.DecimalField(max_digits=12, decimal_places=2)
    

    class Meta:
        managed = False
        db_table = 'carga'

    def __str__(self):
        return self.codigo_carga
    
class Entrega(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    codigo_carga = models.ForeignKey(Carga, null=True,on_delete=models.SET_NULL,blank=True)
    peso_entrega = models.DecimalField(max_digits=9, decimal_places=2)
    valor_entrega = models.DecimalField(max_digits=12, decimal_places=2)
    cidade = models.CharField(max_length=30)
    dificuldade = models.BooleanField()
    cliente = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'entrega'

    def __str__(self):
        return self.id_entrega

class EntregaDistribuidora(models.Model):
    id_entrega = models.ForeignKey(Entrega,on_delete=models.SET_NULL,null=True,blank=True)
    distribuidora = models.CharField(max_length=30,primary_key=True)

    class Meta:
        managed = False
        db_table = 'entrega_distribuidora'
        unique_together = (('id_entrega', 'distribuidora'))

    def __str__(self):
        return self.id_entrega, self.distribuidora