import discord
import asyncio
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from negociacao.services import processar_mensagem_ia, buscar_clientes_para_outbound, confirmar_envio_outbound

load_dotenv()

ANSWER_TIME = 12
TIMEZONE = 'America/Sao_Paulo'
MINI_DELAY = 8
BOT_ID = 1436381275312230575


class MyClient(discord.Client):
    def __init__(self, *, intents, **options):
        self.messages = {}
        self.typing = {}        
        super().__init__(intents=intents, **options)

    async def startConversation(self, discord_id, content, user_id, initial_value=None ):
        user = await self.fetch_user(discord_id)
        if user:
            print(f"Enviando mensagem para {user}")
            await user.send(content)
            if initial_value is not None:
                await confirmar_envio_async(user_id, initial_value, content)
        else:
            print("Não conseguiu localizar o usuário.")

    async def running_bot(self):
        while True:            
            clientes = await buscar_clientes_async()
            print(clientes)
            if clientes:
                for cliente in clientes:
                    self.loop.create_task(
                        self.startConversation(cliente['discord_id'], cliente['mensagem_texto'], cliente['id'], cliente['valor_divida'])
                    )
            await asyncio.sleep(60)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Teste inicial (opcional)
        # await self.startConversation('275275075345973250', "Olá, isso é um teste por enquanto")
        self.loop.create_task(self.running_bot())

    async def on_raw_typing(self, payload):
        if payload.guild_id is None:
            self.typing[payload.user_id] = payload.timestamp

    async def on_message(self, message):
        content_struct = {"content": message.content, "time": message.created_at}

        if message.author.id == BOT_ID:
            return

        if message.author.id not in self.messages:
            self.messages[message.author.id] = [content_struct]
            await asyncio.sleep(ANSWER_TIME)

            while True:
                if message.author.id in self.typing:
                    diff_time = datetime.now(pytz.timezone(TIMEZONE)) - self.typing[message.author.id].astimezone(
                        pytz.timezone(TIMEZONE)
                    )
                    if diff_time.seconds > MINI_DELAY:
                        break
                    await asyncio.sleep(MINI_DELAY)
                
                if message.author.id in self.messages:
                    break     

            content = " ".join([text["content"] for text in self.messages[message.author.id]])
            print(f"Teste conteúdo: {content} ")
            resposta = await processar_mensagem_async(str(message.author.id), content)

            if resposta:
                await message.channel.send(resposta)

            del self.messages[message.author.id]

        else:
            self.messages[message.author.id].append(content_struct)


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.dm_typing = True
intents.dm_messages = True
processar_mensagem_async = sync_to_async(processar_mensagem_ia)
buscar_clientes_async = sync_to_async(buscar_clientes_para_outbound)
confirmar_envio_async = sync_to_async(confirmar_envio_outbound)

class Command(BaseCommand):
    help = "Roda o bot do Discord"

    def handle(self, *args, **options):
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise Exception("Variável de ambiente DISCORD_TOKEN não encontrada!")

        client = MyClient(intents=intents)
        client.run(token)
