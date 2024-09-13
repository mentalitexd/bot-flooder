import discord
from discord.ext import commands
import asyncio
import os
import sys
from colorama import Fore, Style, init

# colorama için başlatma işlemi (Windows için gerekli)
init(autoreset=True)

# intents (izinler) için gerekli ayarlar
intents = discord.Intents.all()

# tokens.txt dosyasından tokenleri okuyarak bir listeye ekliyoruz
def load_tokens():
    with open('tokens.txt', 'r') as file:
        tokens = [line.strip() for line in file.readlines()]
    return tokens

# Konsolu temizlemek için fonksiyon (Windows ve Unix için uyumlu)
def clear_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix (Linux/Mac)
        os.system('clear')

# Banner oluşturma
def print_banner():
    clear_console()  # Konsolu temizle
    print(Fore.BLUE + "===============================")
    print(Fore.BLUE + "Mentalite Tarafından Yapılmıştır")
    print(Fore.BLUE + "===============================\n")
    print(Fore.YELLOW + "1. Tokenleri Aktif Et")
    print(Fore.YELLOW + "0. Çıkış Yap\n")

# Botu başlatan fonksiyon
async def start_bot(token):
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} ({token[:5]}...) is online!')

    # !dm komutu, belirtilen kullanıcıya mesaj gönderir
    @bot.command()
    async def dm(ctx, user_id: int, *, message):
        user = bot.get_user(user_id)
        if user:
            await ctx.send(f"How many times do you want to send the message to {user}?")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30)
                message_count = int(response.content)
                
                for _ in range(message_count):
                    await user.send(message)
                    
                await ctx.send(f'Successfully sent {message_count} message(s) to {user}!')
                
            except asyncio.TimeoutError:
                await ctx.send("You didn't respond in time. Command cancelled.")
            
        else:
            await ctx.send("User not found.")

    await bot.start(token)

# Tüm botları aynı anda başlatmak için asyncio kullanıyoruz
async def main():
    tokens = load_tokens()  # Tokenleri dosyadan yüklüyoruz
    await asyncio.gather(*(start_bot(token) for token in tokens))  # Tüm tokenleri başlatıyoruz

# Ana işlem akışı
def run_tool():
    while True:
        print_banner()  # Banner ve seçenekleri göster
        choice = input(Fore.CYAN + "Seçiminizi yapın: ")  # Kullanıcıdan giriş al
        if choice == '1':
            # Tokenleri aktif et
            print(Fore.GREEN + "Tokenler aktif ediliyor...\n")
            asyncio.run(main())  # Tokenleri çalıştır
        elif choice == '0':
            # Çıkış yap
            print(Fore.RED + "Çıkış yapılıyor...")
            sys.exit()  # Programı kapat
        else:
            print(Fore.RED + "Geçersiz seçim! Tekrar deneyin.\n")

# Aracı başlatıyoruz
run_tool()
