import discord
import os 
import re
import dotenv
# Load the enviroment variables
dotenv.load_dotenv()
Discord_Token = os.getenv("DISCORD_TOKEN")
Command_Prefix = os.getenv("PREFIX")
Chloe_Id = int(os.getenv("CHLOE"))
# Intents
intents = discord.Intents.default()
intents.message_content = True
# 8p
class Cwient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.TARGETS = {}
        self.RESPONSE = "8p"
    def contains_target_emoji(self, message):
        '''Get all emojis in a message and check if the trigger is contained within it
            using sillyness >w<
        '''
        emojis = re.findall(r'<:\w*:\d*>', message.content)
        emojis = set([(e.split(':')[1].replace('>', '')) for e in emojis])
        return len(emojis.intersection(self.TARGETS)) != 0
    def add_target(self, args):
        if len(args) >= 2:
            self.TARGETS.add(' '.join(args[1:]))
    def remove_target(self, args):
        if len(args) >= 2:
            to_remove = ' '.join(args[1:])
            self.TARGETS.remove(to_remove)
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        is_chloe = message.author.id == Chloe_Id
        is_admin = message.author.guild_permissions.administrator
        # we will handle commands in this way for now
        if message.content.startswith(Command_Prefix):
            args = message.content.split(' ')
            if args[0] == Command_Prefix+'add_target' and is_admin: self.add_target(args)
            elif args[0] == Command_Prefix+'die' and is_chloe: await self.close()
            elif args[0] == Command_Prefix+'remove_target' and is_admin: self.remove_target(args)
       # If the message is in the targets, or uses a target emoji (8p), respond with 8p for that guild
        if message.content.lower() in self.TARGETS or self.contains_target_emoji(message):
            # get the 8p emote from the current guild (more robust than hardcoding its ID for Ted's Server)
            emoji = list(filter(lambda e: e.name==self.RESPONSE, message.guild.emojis))
            if len(emoji) == 1:
                await message.channel.send(emoji[0])
            else: await message.channel.send("8p")
    async def on_ready(self):
        print("Weady to 8p")

# Wun the Cwient
if __name__ == "__main__":
    cwient = Cwient()
    # Read in the targets 
    with open("src/targets.out", 'r') as targets:
        cwient.TARGETS = set(targets.read().split('\n'))
    cwient.run(Discord_Token)
    # serialize the set of targets so that it persists across sessions
    with open("src/targets.out", 'w') as outfile:
        outfile.write('\n'.join([x for x in cwient.TARGETS]))