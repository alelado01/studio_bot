import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os


from discord import __version__ as discord_version
print(f"discord.py version: {discord_version}")

intents = discord.Intents.default()

if discord_version >= '2.0.0':
    intents.message_content = True
else:
    intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
allowed_mentions = discord.AllowedMentions(everyone = True)

is_studying = False
end_time = None
remaining_time = None
paused = False



@bot.event
async def on_ready():
    print(f'{bot.user.name} è entrato nel Server per farti studiare!')



@bot.command(name='study')
async def set_studytime(ctx, study_minutes: int, break_minutes: int):
    global is_studying, end_time
    is_studying = True
    await ctx.send(f'Certo {ctx.author}, ho impostato degli intervalli di studio di {study_minutes} minuti con delle pause di {break_minutes} minuti.\nNon stare a guardare quanto tempo manca! Ti manderò un messaggio quando puoi smettere e quando puoi ripartire')

    while is_studying:
        # Inizio della sessione di studio
        end_time = datetime.now() + timedelta(minutes=study_minutes)
        await ctx.send(f'È l\'ora di studiare! 📚\nTi riposerai tra {study_minutes} minuti')
        await asyncio.sleep(study_minutes * 60)

        if not is_studying:
            break

        if paused:
            while paused:
                await asyncio.sleep(1)

        # Fine della sessione di studio
        await ctx.send(f'Sessione di studio finita! Sfrutta al massimo i {break_minutes} minuti di riposo che hai! 🛋️')

        # Inizio della pausa
        end_time = datetime.now() + timedelta(minutes=break_minutes)
        await asyncio.sleep(break_minutes * 60)

        if not is_studying:
            break

        if paused:
            while paused:
                await asyncio.sleep(1)    

        # Fine della pausa
        await ctx.send(f'Ti sei riposato abbastanza! Torna a studiare 📚')



@bot.command(name='groupstudy')
async def group_study(ctx, study_minutes: int, break_minutes: int):
    global is_studying, end_time
    is_studying = True
    await ctx.send(f'{ctx.message.guild.default_role}, ho impostato degli intervalli di studio di {study_minutes} minuti con delle pause di {break_minutes} minuti.\nNon state a guardare quanto tempo manca! Vi manderò un messaggio quando potete smettere e quando potete ripartire')

    while is_studying:
        # Inizio della sessione di studio
        end_time = datetime.now() + timedelta(minutes=study_minutes)
        await ctx.send(f'È l\'ora di studiare! 📚\nVi riposerete tra {study_minutes} minuti')
        await asyncio.sleep(study_minutes * 60)

        if not is_studying:
            break

        if paused:
            while paused:
                await asyncio.sleep(1)

        # Fine della sessione di studio
        await ctx.send(f'Sessione di studio finita! Sfruttate al massimo i {break_minutes} minuti di riposo che avete! 🛋️')

        # Inizio della pausa
        end_time = datetime.now() + timedelta(minutes=break_minutes)
        await asyncio.sleep(break_minutes * 60)

        if not is_studying:
            break

        if paused:
            while paused:
                await asyncio.sleep(1)    

        # Fine della pausa
        await ctx.send(f'Vi siete riposati abbastanza! Tornate a studiare 📚')



@bot.command(name='pause')
async def pause_study(ctx):
    global paused, remaining_time
    if paused:
        ctx.send('Il timer è già in pausa!')
    if not paused and is_studying:
        paused = True
        remaining_time = end_time - datetime.now()
        await ctx.send('Il timer è stato messo in pausa.')
    else:
        await ctx.send('Non è stato impostato alcun timer! Usa il comando !study per iniziare.')


@bot.command(name='resume')
async def resume_study(ctx):
    global paused, end_time
    if not paused:
        await ctx.send('Il timer non è in pausa!')
    else:
        paused=False
        end_time = datetime.now() + remaining_time
        await ctx.send('Il timer è stato ripreso.')


@bot.command(name='countdown')
async def countdown(ctx):
    global end_time, remaining_time, paused
    
    if paused:
        if remaining_time and remaining_time.total_seconds() > 0:
            minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)
            await ctx.send(f'Il timer è in pausa e il countdown è fermo a {minutes} minuti e {seconds} secondi.')
        else:
            await ctx.send('Il timer è in pausa, ma non ci sono secondi rimanenti.')
        return
    
    if end_time:
        remaining_time = end_time - datetime.now()
        if remaining_time.total_seconds() > 0:
            minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)
            await ctx.send(f'Tempo rimanente: {minutes} minuti e {seconds} secondi.')
        else:
            await ctx.send('Il timer è scaduto!')
            end_time = None  # Resetta il timer scaduto
    else:
        await ctx.send('Non è stato impostato alcun timer! Usa il comando !study per iniziare.')



bot.remove_command('help')



@bot.command(name='help')
async def help_command(ctx):
    help_text = """
**Ecco un elenco di comandi disponibili:**

**!study <study_minutes> <break_minutes>**  
Inizia una sessione di studio con un timer per la durata specificata in minuti.  
Esempio: `!study 25 5` avvia una sessione di studio di 25 minuti con una pausa di 5 minuti.

**!groupstudy <study_minutes> <break_minutes>**  
Inizia una sessione di studio per tutti i membri del server, con un timer per la durata specificata in minuti.  
Esempio: `!groupstudy 25 5` avvia una sessione di studio di 25 minuti con una pausa di 5 minuti per tutti.

**!pause**  
Mette in pausa il timer di studio o pausa corrente.  
Esempio: `!pause` mette in pausa il timer.

**!resume**  
Riprende il timer di studio o pausa che è stato messo in pausa.  
Esempio: `!resume` riprende il timer dal punto in cui era stato messo in pausa.

**!countdown**  
Mostra il tempo rimanente per la sessione di studio o di pausa corrente.  
Esempio: `!countdown` mostra quanti minuti e secondi restano nella sessione corrente.

**!help**  
Mostra questo messaggio di aiuto con la descrizione di tutti i comandi disponibili.
    """
    await ctx.send(help_text)



token = os.getenv("DISCORD_TOKEN")

if token:
    bot.run(token)
else:
    print("Errore: variabile d'ambiente DISCORD_TOKEN non trovata.")
        
bot.run(token)
