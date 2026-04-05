import discord
from discord.ext import commands
import subprocess
import os

from dotenv import load_dotenv

load_dotenv()

class ServerTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ENC = os.getenv('ENCRYPT_PASS')
        self.ASC = int(os.getenv('ASC_USER_ID'))
        self.APS = int(os.getenv('APS_USER_ID'))

    @commands.command(name="getip")
    async def get_server_ip(self, self_ctx): # Puedes llamarlo ctx, pero asegúrate que sea el segundo
        # Usamos self.bot o self.ASC_USER_ID siempre con el prefijo 'self.'
        allowed = [self.ASC, self.APS]
        
        if self_ctx.author.id not in allowed:
            return await self_ctx.send("No tienes permisos.")

        try:
            # Ejecutar curl
            raw_ip = subprocess.check_output(["curl", "-s", "https://ifconfig.me", "-4"]).decode("utf-8").strip()

            # Encriptar (usando self.ENCRYPT_PASS correctamente)
            encrypt_cmd = f"echo '{raw_ip}' | openssl enc -aes-256-cbc -a -salt -pass pass:'{self.ENC}' -pbkdf2"
            encrypted_ip = subprocess.check_output(encrypt_cmd, shell=True).decode("utf-8").strip()

            embed = discord.Embed(
                title="🔐 IP del servidor (Encriptada)",
                description=f"```\n{encrypted_ip}\n```",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Desencripta con openssl y tu clave.")

            await self_ctx.send(embed=embed)

        except Exception as e:
            await self_ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(ServerTools(bot))
