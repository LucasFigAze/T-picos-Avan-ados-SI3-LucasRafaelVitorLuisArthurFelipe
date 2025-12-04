import discord
import asyncio
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ANSWER_TIME=12
TIMEZONE= 'America/Sao_Paulo'
MINI_DELAY=8 # Deu para perceber no discord aqui
BOT_ID=1436381275312230575
 
class MyClient(discord.Client):    
    def __init__(self, *, intents, **options):
        self.messages = {}
        self.typing   = {}
        super().__init__(intents=intents, **options)

    def scheduleStartConversation(self, user_id, installments):        
        if self.is_ready():            
            self.loop.create_task(self.startConversation(user_id, installments))
            return True
        return False

    async def startConversation(self, user_id, installments):
        user = await self.fetch_user(user_id)
        if user:
            print(user)
            await user.send(installments)
        else:
            print("deu ruim aqui")   

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await asyncio.sleep(2)
        self.loop.create_task(self.startConversation('275275075345973250', "Ola, isso é um teste por enquanto"))        

    # async def on_typing(self, channel, user, when):
    #     print(f"{user} está digitando em {channel} às {when}")

    async def on_raw_typing(self, payload):
        if payload.guild_id is not None:
            print("Mensagem de servidor aqui")
        else:
            print(f"adicionou aqui: {payload.timestamp}")
            self.typing[payload.user_id] = payload.timestamp
            # print(payload.timestamp)
            # if payload.user_id not in self.typing.keys():
            #     self.typing[payload.user_id] = [payload.timestamp]
            # else:
            #     self.typing[payload.user_id].append(payload.timestamp)

    async def on_message(self, message):        
        content_struct = {
                "content": message.content, 
                "time": message.created_at
            }                
        if message.author.id == BOT_ID: 
            return
        
        if message.author.id not in self.messages.keys():
            print("primeira mensagem enviada")            
            self.messages[message.author.id] = [content_struct]                                    
            await asyncio.sleep(ANSWER_TIME)
            while True:
                print(self.typing)
                print(message.author.id)                                
                if message.author.id in self.typing:                    
                    diff_time =  datetime.now(pytz.timezone(TIMEZONE)) - self.typing[message.author.id].astimezone(pytz.timezone(TIMEZONE))             
                    print(diff_time)
                    if diff_time.seconds > MINI_DELAY:
                        break                    
                    await asyncio.sleep(MINI_DELAY)
                    

            content = ""
            for text in self.messages[message.author.id]:
                content += text["content"] + " "
            print(content)
            del self.messages[message.author.id]
                                    
        else:
            print(f"{len(self.messages[message.author.id])}° mensagem enviada")
            diff_time = content_struct["time"] - self.messages[message.author.id][0]["time"] 
            print(diff_time.seconds)
            # print((content_struct["time"] - self.messages[message.author.id][0]["time"]))
            self.messages[message.author.id].append(content_struct)        
    

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.dm_typing = True
intents.dm_messages = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))