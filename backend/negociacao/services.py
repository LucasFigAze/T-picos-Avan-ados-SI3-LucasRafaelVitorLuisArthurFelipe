import os
from django.db.models import Sum
from .models import ClienteFinal, Fatura, HistoricoConversa, AcordoProposto
from .chains import negotiation_chain, intention_chain

def processar_mensagem_ia(discord_id, mensagem_usuario):
    """
    Função CENTRAL (Cérebro).
    Recebe o ID do Discord e a mensagem, executa o RAG e retorna a resposta em texto.
    """

    try:
        cliente = ClienteFinal.objects.get(discord_user_id=discord_id)
    except ClienteFinal.DoesNotExist:
        return "Olá! Não localizei seu cadastro vinculado a este Discord. Por favor, entre em contato com o suporte."

    if cliente.status_conversa == 'HANDOFF':
        return None

    if cliente.status_conversa == 'NAO_INICIADO':
        cliente.status_conversa = 'NEGOCIANDO'
        cliente.save()

    # Coleta de Dados do Banco (Retrieval)
    faturas = Fatura.objects.filter(contrato__cliente_final=cliente, status='PENDENTE')

    if not faturas.exists():
        return "Consultei seu cadastro e não constam faturas pendentes. Obrigado!"

    valor_total_atual = faturas.aggregate(Sum('valor_original'))['valor_original__sum'] or 0

    # 5. Validação de Integridade (Data Drift)
    msg_aviso_valor = ""
    if cliente.valor_total_em_negociacao and cliente.valor_total_em_negociacao != valor_total_atual:
        msg_aviso_valor = f"(Aviso automático: O valor da sua dívida foi atualizado no sistema para R$ {valor_total_atual:,.2f}). "
        cliente.valor_total_em_negociacao = valor_total_atual
        cliente.save()

    if not cliente.valor_total_em_negociacao:
        cliente.valor_total_em_negociacao = valor_total_atual
        cliente.save()

    # Preparação do Contexto (Augmentation)
    politica = cliente.empresa_cliente.politica

    historico_msgs = HistoricoConversa.objects.filter(cliente_final=cliente).order_by('-timestamp')[:10]

    historico_texto = "\n".join([f"{h.autor}: {h.mensagem}" for h in reversed(historico_msgs)])

    detalhes_faturas = "\n".join([f"- Fatura #{f.id}: R$ {f.valor_original:,.2f} (Venc: {f.data_vencimento.strftime('%d/%m/%Y')})" for f in faturas])

    # Geração da Resposta (Generation)
    resposta_bot = negotiation_chain.invoke({
        "nome_empresa": cliente.empresa_cliente.nome_empresa,
        "prompt_base_persona": politica.prompt_base_persona,
        "nome_cliente": cliente.nome_completo,
        "valor_divida": f"{valor_total_atual:,.2f}",
        "detalhes_faturas": detalhes_faturas,
        "max_desconto": politica.max_desconto_avista,
        "max_parcelas": politica.max_parcelas,
        "juros": politica.juros_parcelamento,
        "historico": historico_texto,
        "input": mensagem_usuario
    })

    if msg_aviso_valor:
        resposta_bot = f"{msg_aviso_valor}\n{resposta_bot}"

    HistoricoConversa.objects.create(cliente_final=cliente, autor='USER', mensagem=mensagem_usuario)
    HistoricoConversa.objects.create(cliente_final=cliente, autor='BOT', mensagem=resposta_bot)

    # Análise de Intenção (Handoff)
    intencao = intention_chain.invoke({"input": mensagem_usuario})

    if "ACORDO" in intencao.upper():
        cliente.status_conversa = 'HANDOFF'
        cliente.save()

        acordo = AcordoProposto.objects.create(
            cliente_final=cliente,
            valor_total_original=valor_total_atual,
            valor_negociado=valor_total_atual,
            valor_parcela=valor_total_atual,
            status='PENDENTE'
        )
        acordo.faturas_incluidas.set(faturas)

        msg_final = f"{resposta_bot}\n\n✅ **Acordo Registrado!**\nSua proposta (ID #{acordo.id}) foi enviada para validação. Aguarde nosso retorno."

        ultimo = HistoricoConversa.objects.filter(cliente_final=cliente, autor='BOT').last()
        ultimo.mensagem = msg_final
        ultimo.save()

        return msg_final

    return resposta_bot


def buscar_clientes_para_outbound():
    """
    Busca clientes que ainda não foram contatados (NAO_INICIADO) e têm Discord ID.
    Usado pelo loop do bot.
    """
    clientes = ClienteFinal.objects.filter(
        status_conversa='NAO_INICIADO',
        discord_user_id__isnull=False
    ).exclude(discord_user_id='')[:5]

    lista_para_envio = []
    for c in clientes:
        faturas = Fatura.objects.filter(contrato__cliente_final=c, status='PENDENTE')
        valor_total = faturas.aggregate(Sum('valor_original'))['valor_original__sum'] or 0

        if valor_total > 0:
            lista_para_envio.append({
                'id': c.id,
                'discord_id': c.discord_user_id,
                'nome': c.nome_completo,
                'valor_divida': valor_total,
                'empresa': c.empresa_cliente.nome_empresa
            })

    return lista_para_envio


def confirmar_envio_outbound(cliente_id, valor_inicial):
    """
    Atualiza o cliente para NEGOCIANDO após o bot enviar a msg inicial com sucesso.
    """
    try:
        cliente = ClienteFinal.objects.get(id=cliente_id)
        cliente.status_conversa = 'NEGOCIANDO'
        cliente.valor_total_em_negociacao = valor_inicial
        cliente.save()

        HistoricoConversa.objects.create(
            cliente_final=cliente,
            autor='BOT',
            mensagem=f"[SISTEMA] Mensagem inicial de cobrança enviada. Valor: R$ {valor_inicial}"
        )
        return True
    except Exception as e:
        print(f"Erro ao atualizar cliente {cliente_id}: {e}")
        return False
