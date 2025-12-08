from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from negociacao.models import EmpresaCliente, PoliticaNegociacao, ClienteFinal, Contrato, Fatura, HistoricoConversa, AcordoProposto

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para negociação'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Limpando dados antigos...'))
        AcordoProposto.objects.all().delete()
        HistoricoConversa.objects.all().delete()
        Fatura.objects.all().delete()
        Contrato.objects.all().delete()
        ClienteFinal.objects.all().delete()
        PoliticaNegociacao.objects.all().delete()
        EmpresaCliente.objects.all().delete()

        self.stdout.write('Criando novos dados...')

        # 1. Empresa e Política
        empresa = EmpresaCliente.objects.create(
            nome_empresa="Banco Capyba S.A.",
            cnpj="12345678000199"
        )

        PoliticaNegociacao.objects.create(
            empresa_cliente=empresa,
            prompt_base_persona="Você é o Fin, um assistente virtual empático e focado em soluções. Use tom profissional mas acolhedor.",
            max_desconto_avista=25.00,
            max_parcelas=12,
            juros_parcelamento=1.99
        )

        # 2. Cliente
        discord_id_teste = "447526544387211264"

        cliente = ClienteFinal.objects.create(
            empresa_cliente=empresa,
            nome_completo="João da Silva",
            cpf="11122233344",
            email="joao@teste.com",
            discord_user_id=discord_id_teste,
            status_conversa='NAO_INICIADO'
        )

        # 3. Dívidas (Cenário: 2 Faturas atrasadas)
        contrato_cartao = Contrato.objects.create(
            cliente_final=cliente,
            codigo_contrato="CARTAO-GOLD-888",
            descricao="Cartão de Crédito Gold"
        )

        Fatura.objects.create(
            contrato=contrato_cartao,
            valor_original=Decimal("850.00"),
            data_vencimento=timezone.now().date() - timezone.timedelta(days=45), # Venceu há 45 dias
            status='PENDENTE'
        )

        Fatura.objects.create(
            contrato=contrato_cartao,
            valor_original=Decimal("150.00"),
            data_vencimento=timezone.now().date() - timezone.timedelta(days=15), # Venceu há 15 dias
            status='PENDENTE'
        )

        self.stdout.write(self.style.SUCCESS('✅ Banco populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'👉 ID do Discord para teste: {discord_id_teste}'))
        self.stdout.write(self.style.SUCCESS(f'👉 Valor total da dívida: R$ 1.000,00'))