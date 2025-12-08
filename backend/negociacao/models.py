from django.db import models
from django.contrib.auth.models import User


class EmpresaCliente(models.Model):
    nome_empresa = models.CharField(max_length=255, unique=True, help_text="Nome da empresa credora")
    cnpj = models.CharField(max_length=14, unique=True, help_text="CNPJ da empresa credora")
    
    class Meta:
        verbose_name = "Empresa Cliente"
        verbose_name_plural = "Empresas Clientes"

    def __str__(self):
        return self.nome_empresa


class PoliticaNegociacao(models.Model):
    empresa_cliente = models.OneToOneField(
        EmpresaCliente, 
        on_delete=models.CASCADE, 
        related_name="politica"
    )
    prompt_base_persona = models.TextField(
        help_text="O prompt base do sistema"
    )
    max_desconto_avista = models.DecimalField(
        max_digits=5, decimal_places=2, default=25.0, help_text="Ex: 25.00 para 25%"
    )
    max_parcelas = models.PositiveIntegerField(default=12, help_text="Ex: 12")
    juros_parcelamento = models.DecimalField(
        max_digits=5, decimal_places=2, default=1.5, help_text="Ex: 1.50 para 1.5% a.m."
    )
    
    class Meta:
        verbose_name = "Política de Negociação"
        verbose_name_plural = "Políticas de Negociação"

    def __str__(self):
        return f"Política de {self.empresa_cliente.nome_empresa}"


class ClienteFinal(models.Model):
    STATUS_CONVERSA_CHOICES = [
        ('NAO_INICIADO', 'Não Iniciado'),
        ('NEGOCIANDO', 'Em Negociação'),
        ('HANDOFF', 'Aguardando Analista'),
        ('CONCLUIDO', 'Acordo Fechado'),
    ]

    empresa_cliente = models.ForeignKey(EmpresaCliente, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, db_index=True)
    email = models.EmailField(blank=True, null=True)
    discord_user_id = models.CharField(
        max_length=100, blank=True, null=True, unique=True, db_index=True,
        help_text="ID do usuário no Discord"
    )

    status_conversa = models.CharField(
        max_length=20,
        choices=STATUS_CONVERSA_CHOICES,
        default='NAO_INICIADO'
    )
    valor_total_em_negociacao = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Valor total da dívida que estava sendo negociado na ÚLTIMA interação."
    )

    class Meta:
        unique_together = ('empresa_cliente', 'cpf')
        verbose_name = "Cliente Final"
        verbose_name_plural = "Clientes Finais"

    def __str__(self):
        return f"{self.nome_completo} ({self.empresa_cliente.nome_empresa})"


class Contrato(models.Model):
    cliente_final = models.ForeignKey(ClienteFinal, on_delete=models.CASCADE, related_name="contratos")
    codigo_contrato = models.CharField(max_length=255, help_text="Código do contrato no ERP de origem")
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
    
    def __str__(self):
        return f"Contrato {self.codigo_contrato} ({self.cliente_final.nome_completo})"


class Fatura(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('NEGOCIANDO', 'Negociando'),
        ('PAGA', 'Paga'),
    ]
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="faturas")
    valor_original = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', db_index=True)

    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"

    def __str__(self):
        return f"Fatura {self.id} - R${self.valor_original} ({self.status})"


class AcordoProposto(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Aprovação'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    cliente_final = models.ForeignKey(ClienteFinal, on_delete=models.CASCADE, related_name="acordos")

    faturas_incluidas = models.ManyToManyField(Fatura, related_name="acordos_propostos")

    valor_total_original = models.DecimalField(max_digits=10, decimal_places=2)
    valor_negociado = models.DecimalField(max_digits=10, decimal_places=2)
    num_parcelas = models.PositiveIntegerField(default=1)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_proposta = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', db_index=True)

    analista_responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Analista que aprovou/rejeitou",
        limit_choices_to={'is_staff': True}
    )
    observacoes_analista = models.TextField(blank=True, help_text="Notas do analista sobre a aprovação/rejeição")

    notificado_discord = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = "Acordo Proposto"
        verbose_name_plural = "Acordos Propostos"

    def __str__(self):
        return f"Acordo {self.id} - {self.cliente_final.nome_completo} ({self.status})"


class HistoricoConversa(models.Model):
    AUTOR_CHOICES = [('USER', 'Usuário'), ('BOT', 'Bot')]

    cliente_final = models.ForeignKey(ClienteFinal, on_delete=models.CASCADE, related_name="historico")
    timestamp = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=10, choices=AUTOR_CHOICES)
    mensagem = models.TextField()

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Histórico de Conversa"
        verbose_name_plural = "Históricos de Conversa"

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.autor}: {self.mensagem}"