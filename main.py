import discord
from discord.ext import commands
import asyncio
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

intents = discord.Intents.all()

def load_tokens():
    with open('tokens.txt', 'r') as file:
        tokens = [line.strip() for line in file.readlines()]
    return tokens

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    clear_console()
    print(Fore.BLUE + "===============================")
    print(Fore.BLUE + "Mentalite Tarafından Yapılmıştır")
    print(Fore.BLUE + "===============================\n")
    print(Fore.YELLOW + "1. Tokenleri Aktif Et")
    print(Fore.YELLOW + "0. Çıkış Yapınn")

async def start_bot(token):
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} ({token[:5]}...) Aktif!')

    @bot.command()
    async def dm(ctx, user_id: int, *, message):
        user = bot.get_user(user_id)
        if user:
            await ctx.send(f"{user} kullanıcısına mesajı kaç kez göndermek istiyorsunuz?")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30)
                message_count = int(response.content)
                
                for _ in range(message_count):
                    await user.send(message)
                    
                await ctx.send(f'{message_count} mesajı {user} adlı kullanıcıya başarıyla gönderildi!')
                
            except asyncio.TimeoutError:
                await ctx.send("Zamanında cevap vermediniz. Komut iptal edildi.")
            
        else:
            await ctx.send("Kullanıcı bulunamadı.")

    await bot.start(token)

async def main():
    tokens = load_tokens()
    await asyncio.gather(*(start_bot(token) for token in tokens))

# Ana işlem akışı
def run_tool():
    while True:
        print_banner()
        choice = input(Fore.CYAN + "Seçiminizi yapın: ")
        if choice == '1':
            print(Fore.GREEN + "Tokenler aktif ediliyor...\n")
            asyncio.run(main())
        elif choice == '0':
            print(Fore.RED + "Çıkış yapılıyor...")
            sys.exit()
        else:
            print(Fore.RED + "Geçersiz seçim! Tekrar deneyin.\n")

run_tool()
