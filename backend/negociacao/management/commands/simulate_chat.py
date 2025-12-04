from django.core.management.base import BaseCommand
from negociacao.services import processar_mensagem_ia, acionar_outbound_manual
from negociacao.models import ClienteFinal


class Command(BaseCommand):
    help = 'Simulador de Chat Outbound'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('--- SIMULADOR FIN.NEGOCIA (OUTBOUND) ---'))

        discord_id = input("ID do Discord (Enter para 'simulacao_user_001'): ").strip() or "simulacao_user_001"

        try:
            cliente = ClienteFinal.objects.get(discord_user_id=discord_id)
            self.stdout.write(self.style.SUCCESS(f"Cliente: {cliente.nome_completo} | Status: {cliente.status_conversa}"))

            # --- FLUXO OUTBOUND ---
            if cliente.status_conversa == 'NAO_INICIADO':
                self.stdout.write(self.style.WARNING("\n[Iniciando Fluxo Outbound...]"))

                # Chama nossa nova função que gera a msg, salva no banco e muda status
                msg_inicial = acionar_outbound_manual(discord_id)

                if msg_inicial:
                    print(f"\n🤖 Bot (Mensagem Ativa):\n{msg_inicial}\n")
                else:
                    self.stdout.write(self.style.ERROR("Erro ao gerar outbound."))

            # Se o cliente já estava negociando, recuperamos o histórico
            elif cliente.status_conversa == 'NEGOCIANDO':
                print("\n[Continuando conversa existente...]")

        except ClienteFinal.DoesNotExist:
            self.stdout.write(self.style.ERROR("Cliente não encontrado. Rode o seed_db primeiro."))
            return

        self.stdout.write("-" * 50)
        self.stdout.write("Agora é sua vez. Responda ao Bot (ou 'sair'):\n")

        # Loop de Conversa
        while True:
            try:
                texto_usuario = input(self.style.WARNING("Você: "))
                if texto_usuario.lower() in ['sair', 'exit']: break

                self.stdout.write(self.style.HTTP_INFO("(IA processando...)"))

                resposta = processar_mensagem_ia(discord_id, texto_usuario)

                if resposta:
                    print(f"\n🤖 Bot:\n{resposta}\n")
                else:
                    print("\n[Bot encerrou a conversa/Handoff]\n")
                    break

            except KeyboardInterrupt:
                break
