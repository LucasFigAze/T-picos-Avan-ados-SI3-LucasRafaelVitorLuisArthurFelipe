from django.contrib import admin
from django.utils.html import format_html
from .models import (
    EmpresaCliente,
    PoliticaNegociacao,
    ClienteFinal,
    Contrato,
    Fatura,
    AcordoProposto,
    HistoricoConversa
)


@admin.action(description='✅ APROVAR acordos selecionados')
def marcar_aprovado(modeladmin, request, queryset):
    """
    Define o status como APROVADO e atribui o analista logado.
    """
    queryset.update(status='APROVADO', analista_responsavel=request.user)
    modeladmin.message_user(request, f"{queryset.count()} acordos foram aprovados com sucesso.")


@admin.action(description='❌ REJEITAR acordos selecionados')
def marcar_rejeitado(modeladmin, request, queryset):
    """
    Define o status como REJEITADO e atribui o analista logado.
    """
    queryset.update(status='REJEITADO', analista_responsavel=request.user)
    modeladmin.message_user(request, f"{queryset.count()} acordos foram rejeitados.")


class PoliticaInline(admin.StackedInline):
    """Permite editar a Política direto na tela da Empresa"""
    model = PoliticaNegociacao
    can_delete = False
    verbose_name_plural = 'Política de Negociação'


class FaturaInline(admin.TabularInline):
    """Permite ver/editar Faturas direto na tela do Contrato"""
    model = Fatura
    extra = 0
    fields = ('valor_original', 'data_vencimento', 'status')
    readonly_fields = ('status',)


class HistoricoInline(admin.TabularInline):
    """Mostra o histórico de conversa dentro da tela do Cliente"""
    model = HistoricoConversa
    extra = 0
    readonly_fields = ('timestamp', 'autor', 'mensagem')
    can_delete = False
    max_num = 0


@admin.register(EmpresaCliente)
class EmpresaClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_empresa', 'cnpj', 'ver_politica')
    search_fields = ('nome_empresa', 'cnpj')
    inlines = [PoliticaInline]

    def ver_politica(self, obj):
        return "Configurada" if hasattr(obj, 'politica') else "Pendente"
    ver_politica.short_description = "Política"


@admin.register(ClienteFinal)
class ClienteFinalAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'empresa_cliente', 'status_conversa', 'discord_user_id')
    list_filter = ('empresa_cliente', 'status_conversa')
    search_fields = ('nome_completo', 'cpf', 'discord_user_id', 'email')
    inlines = [HistoricoInline]

    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('empresa_cliente', 'nome_completo', 'cpf', 'email')
        }),
        ('Integração & Estado', {
            'fields': ('discord_user_id', 'status_conversa', 'valor_total_em_negociacao')
        }),
    )


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('codigo_contrato', 'cliente_final', 'get_empresa')
    search_fields = ('codigo_contrato', 'cliente_final__nome_completo', 'cliente_final__cpf')
    list_filter = ('cliente_final__empresa_cliente',)
    inlines = [FaturaInline]

    def get_empresa(self, obj):
        return obj.cliente_final.empresa_cliente
    get_empresa.short_description = 'Empresa'


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'contrato', 'valor_original', 'data_vencimento', 'status_colorido')
    list_filter = ('status', 'data_vencimento', 'contrato__cliente_final__empresa_cliente')
    search_fields = ('contrato__codigo_contrato', 'contrato__cliente_final__cpf')

    def status_colorido(self, obj):
        colors = {
            'PENDENTE': 'orange',
            'NEGOCIANDO': 'blue',
            'PAGA': 'green',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colorido.short_description = 'Status'


@admin.register(AcordoProposto)
class AcordoPropostoAdmin(admin.ModelAdmin):
    """
    Tela principal do Analista Humano.
    """
    list_display = (
        'id',
        'cliente_final',
        'valor_negociado',
        'num_parcelas',
        'status_badge',
        'analista_responsavel',
        'data_proposta'
    )
    list_filter = ('status', 'data_proposta', 'cliente_final__empresa_cliente')
    search_fields = ('cliente_final__nome_completo', 'cliente_final__cpf')

    filter_horizontal = ('faturas_incluidas',)

    actions = [marcar_aprovado, marcar_rejeitado]

    readonly_fields = ('data_proposta',)

    def status_badge(self, obj):
        icons = {
            'PENDENTE': '⏳ Pendente',
            'APROVADO': '✅ Aprovado',
            'REJEITADO': '❌ Rejeitado',
        }
        return icons.get(obj.status, obj.status)
    status_badge.short_description = 'Status'


@admin.register(HistoricoConversa)
class HistoricoConversaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'cliente_final', 'autor', 'mensagem_curta')
    list_filter = ('autor', 'timestamp')
    search_fields = ('mensagem', 'cliente_final__nome_completo')
    readonly_fields = ('timestamp', 'cliente_final', 'autor', 'mensagem')

    def mensagem_curta(self, obj):
        return obj.mensagem[:80] + "..." if len(obj.mensagem) > 80 else obj.mensagem
    mensagem_curta.short_description = 'Mensagem'
