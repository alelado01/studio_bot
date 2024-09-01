import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

is_studying = False  # Inizialmente non stiamo studiando
end_time = None  # Variabile per memorizzare l'orario di fine
remaining_time = None  # Variabile per memorizzare il tempo rimanente
paused = False  # Inizialmente non è in pausa



@bot.event
async def on_ready():
    print(f'{bot.user.name} è entrato nel Server per farti studiare!')

@bot.command(name='set_studytime')
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
        await ctx.send('Non è stato impostato alcun timer! Usa il comando !set_studytime per iniziare.')


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
        await ctx.send('Non è stato impostato alcun timer! Usa il comando !set_studytime per iniziare.')





        
bot.run('MTI3OTgyMjczODAyMTgxNDMxNQ.GyNkX0.2ro8qlEXffzwNFwHCliEnlAj5BvLM51sM4BdUk')
