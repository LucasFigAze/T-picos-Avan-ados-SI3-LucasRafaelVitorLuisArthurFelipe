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

    tabela_calculada = calcular_tabela_parcelas(
        valor_total_atual, 
        politica.max_parcelas, 
        politica.juros_parcelamento
    )

    historico_msgs = HistoricoConversa.objects.filter(cliente_final=cliente).order_by('-timestamp')[:10]

    ultimo_bot_obj = HistoricoConversa.objects.filter(
        cliente_final=cliente,
        autor='BOT'
    ).order_by('-id').first()
    ultima_msg_bot_texto = ultimo_bot_obj.mensagem if ultimo_bot_obj else "Nenhuma mensagem anterior."

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
        "tabela_calculada": tabela_calculada,
        "historico": historico_texto,
        "input": mensagem_usuario
    })

    if msg_aviso_valor:
        resposta_bot = f"{msg_aviso_valor}\n{resposta_bot}"

    # 8. Análise de Intenção PRIMEIRO (Antes de salvar histórico)
    # Verificamos se ESSA mensagem do usuário já fecha o acordo
    intencao = intention_chain.invoke({"input": mensagem_usuario, "ultima_mensagem_bot": ultima_msg_bot_texto})

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

        msg_final = (
            f"Perfeito! Entendi que fechamos o acordo.\n\n"
            f"✅ **Acordo Registrado com Sucesso!**\n"
            f"Sua proposta (ID #{acordo.id}) foi enviada para nosso analista validar e gerar o boleto/link.\n\n"
            f"Assim que estiver pronto, eu te chamo por aqui com o documento para pagamento. Obrigado!"
        )

        # Salva o histórico com a mensagem final correta
        HistoricoConversa.objects.create(cliente_final=cliente, autor='USER', mensagem=mensagem_usuario)
        HistoricoConversa.objects.create(cliente_final=cliente, autor='BOT', mensagem=msg_final)

        return msg_final

    # Se não é acordo, salva e retorna a resposta normal do chat
    HistoricoConversa.objects.create(cliente_final=cliente, autor='USER', mensagem=mensagem_usuario)
    HistoricoConversa.objects.create(cliente_final=cliente, autor='BOT', mensagem=resposta_bot)

    return resposta_bot


def gerar_texto_inicial(nome_cliente, valor_total, nome_empresa):
    """
    Gera o texto padrão para iniciar a conversa.
    """
    return (
        f"Olá **{nome_cliente}**! Aqui é o Finegocia, parceiro do {nome_empresa}.\n\n"
        f"Consta em nosso sistema um débito pendente atualizado de **R$ {valor_total:,.2f}**.\n"
        "Estou aqui para te ajudar a resolver isso com condições especiais e limpar seu nome.\n\n"
        "Podemos conversar sobre um plano de pagamento agora?"
    )


def buscar_clientes_para_outbound():
    """
    Busca clientes para o loop automático do bot.
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
            # Geramos o texto aqui para o bot enviar
            msg_texto = gerar_texto_inicial(c.nome_completo, valor_total, c.empresa_cliente.nome_empresa)

            lista_para_envio.append({
                'id': c.id,
                'discord_id': c.discord_user_id,
                'valor_divida': valor_total,
                'mensagem_texto': msg_texto
            })

    return lista_para_envio


def confirmar_envio_outbound(cliente_id, valor_inicial, mensagem_texto):
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
            mensagem=mensagem_texto
        )
        return True
    except Exception as e:
        print(f"Erro ao atualizar cliente {cliente_id}: {e}")
        return False


def acionar_outbound_manual(discord_id):
    """
    Função EXCLUSIVA para o seu Simulador de Terminal.
    Força o envio da mensagem inicial se o cliente estiver NAO_INICIADO.
    """
    try:
        cliente = ClienteFinal.objects.get(discord_user_id=discord_id)

        if cliente.status_conversa == 'NAO_INICIADO':
            # Calcula valor
            faturas = Fatura.objects.filter(contrato__cliente_final=cliente, status='PENDENTE')
            valor_total = faturas.aggregate(Sum('valor_original'))['valor_original__sum'] or 0

            if valor_total > 0:
                # Gera texto
                msg = gerar_texto_inicial(cliente.nome_completo, valor_total, cliente.empresa_cliente.nome_empresa)

                # Confirma e Salva no banco
                confirmar_envio_outbound(cliente.id, valor_total, msg)

                return msg # Retorna o texto para o terminal exibir
            else:
                return "Erro: Cliente sem dívidas pendentes."
        return None # Cliente já estava negociando

    except ClienteFinal.DoesNotExist:
        return "Erro: Cliente não encontrado."


def calcular_tabela_parcelas(valor_total, max_parcelas, taxa_juros_am):
    """
    Gera uma 'Cola' de parcelamento para a IA não alucinar.
    """
    tabela = []
    i = float(taxa_juros_am) / 100
    valor = float(valor_total)

    a_vista = f"- 1x de R$ {valor*0.75:,.2f}"
    tabela.append(a_vista)

    for n in range(2, max_parcelas + 1):
        if i > 0:
            # Fórmula da Tabela Price (PMT)
            fator = (i * ((1 + i) ** n)) / (((1 + i) ** n) - 1)
            valor_parcela = valor * fator
        else:
            valor_parcela = valor / n

        valor_total_final = valor_parcela * n

        linha = f"- {n}x de R$ {valor_parcela:,.2f} (Total com juros: R$ {valor_total_final:,.2f})"
        tabela.append(linha)

    return "\n".join(tabela)
