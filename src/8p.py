import discord
import os 
import re
import dotenv
# Load the enviroment variables
dotenv.load_dotenv()
Discord_Token = os.getenv("DISCORD_TOKEN")
# Possible representations of the emote target
# Going to store these as constants in the event that I want to add more functionality in the future
TARGETS = {'<:8p:1150956242529964052>', ':8p:', '8p'}
RESPONSE = "8p"
# Intents
intents = discord.Intents.default()
intents.message_content = True
# 8p
class Cwient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
    def contains_target_emoji(self, message):
        '''Get all emojis in a message and check if the trigger is contained within it
            using sillyness >w<
        '''
        emojis = re.findall(r'<:\w*:\d*>', message.content)
        emojis = set([(e.split(':')[1].replace('>', '')) for e in emojis])
        return len(emojis.intersection(TARGETS)) != 0
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content.lower() in TARGETS or self.contains_target_emoji(message):
            # get the 8p emote from the current guild (more robust than hardcoding its ID for Ted's Server)
            emoji = list(filter(lambda e: e.name==RESPONSE, message.guild.emojis))
            assert(emoji != None)
            await message.channel.send(emoji[0])
    async def on_ready(self):
        print("Weady to 8p")
# Wun the Cwient
if __name__ == "__main__":
    cwient = Cwient()
    cwient.run(Discord_Token)