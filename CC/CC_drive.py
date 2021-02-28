import discord
from discord.ext import commands
import random,time
from pypinyin import pinyin
import re
# pip install googletrans==4.0.0-rc1
from googletrans import Translator
try:
    translator = Translator(service_urls=['translate.google.com',])
except:
    translator = Translator(service_urls=['translate.google.cn',])

t_jeu = 20
description = "Bot de ClubChineCentraleLyon"
bot = commands.Bot(command_prefix='$', description=description)

with open("spy_db.txt","r",encoding='UTF-8') as f:
    spy_db=f.readlines()
spy_db.pop(0)
with open("dsv_db.txt","r",encoding='UTF-8') as f:
    dsv_db=f.readlines()
dsv_db=dsv_db[1].split(";")
with open("chat_db.txt","r",encoding='UTF-8') as f:
    chat_db=f.readlines()
chat_db.pop(0)
chat_db={re.sub("[,./;'\[\]!@#$%^&*()_+|}{\":<>?\\，。、；‘【】、“：”《》？—！@￥…（）]","",chat.split("///")[0].lower()):chat.split("///")[1] for chat in chat_db}

def split_words(words):
    word_list = ""
    tmp = ""
    for string in words:
        if len(bytes(string, 'utf-8')) == 3 and len(string) == 1:
            if tmp != '':
                word_list += tmp.ljust(6)
                tmp = ""
            word_list += string.ljust(5)
        else:
            tmp += string
    return word_list

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def translate(ctx, *phrase):
    phrase=' '.join([*phrase])
    d=1
    for w in phrase[:3]:
        if ord(w)>11903 and w not in "，！？：‘’“”【】":
            d=0;break
    if d:
        src_="fr";dest_="zh-cn"
    else:
        src_="zh-cn";dest_="fr"
    if dest_=="fr":
        _new_line = re.sub(r'\s', '', phrase)
        _pinyin = ''.join(map(lambda x: x[0].ljust(6), pinyin(_new_line)))
        _lyric = split_words(_new_line)
        _trans = translator.translate(_new_line,src=src_,dest=dest_).text
        await ctx.send('%s\n%s\n%s\n\n' % (_pinyin, _lyric,_trans))
    else:
        _new_line = re.sub(r'\n', '', phrase)
        _trans = translator.translate(_new_line,src=src_,dest=dest_).text
        await ctx.send('%s\n%s\n\n' % (_new_line,_trans))

@bot.command()
async def rule(ctx, *para):
    await ctx.send('Règlements : https://docs.google.com/document/d/1OG6zNvzq_hxXZJT3CkmKmE7j3MM5J5UbhEjsohr9NrQ/edit?usp=sharing')

@bot.command()
async def salut(ctx, *para):
    await ctx.send(f"^w^ Salut, {ctx.author.name} ! Voici CC. Enchantée !")

@bot.command()
async def CC(ctx,*chat):
    chat = ' '.join([*chat])
    try:
        response=chat_db[re.sub("[,./;'\[\]!@#$%^&*()_+|}{\":<>?\\，。、；‘’【】、“：”《》？—！@￥…（）]","",chat).lower()]
        await ctx.send(response)
    except:
        await ctx.send("Pardon, CC est en train d'apprendre comment parler. Je ne comprends pas encore ce que vous disez !")
        
@bot.command()
async def spy(ctx,num: int,*para):
    if int(ctx.channel.id) != 811359562933338142:
        await ctx.send('Pardon, cette commande ne peut fonctionner que dans le channel [游戏室-JEUX].')
    else:
        if int(num)<=2:
            await ctx.send('Coucou ! Il faut au moins 3 joueurs.')
        else:
            await ctx.send(f'Les joueurs tapent "1" ici, svp !');players=[]
            msg=ctx.message;conn=1;t=time.time()
            while time.time()-t<=t_jeu and conn!=0 : 
                async for message in ctx.channel.history(limit=10,after=msg):
                    if "1" in message.content and message.author not in players and message.author!=bot.user:
                        players.append(message.author)
                    msg=message
                    if len(players)==int(num):
                        conn=0;break
            if len(players)<=2:
                await ctx.send('Coucou ! Il faut au moins 3 joueurs.')
            else:
                mots=spy_db[random.randint(0,len(spy_db)-1)].split("--");
                random.shuffle(mots);mot=mots[0];mot_spy=mots[1]
                mots=[mot]*(len(players)-1)+[mot_spy]
                random.shuffle(mots);names=[]
                for i in range(len(players)):
                    await players[i].send(f'Coucou ! Votre mot: {mots[i]}')
                    names.append(players[i].name)
                if len(names)==int(num):
                    await ctx.send(f'Coucou ! {names}, vous pourrez commencer votre jeu !')
                else:
                    await ctx.send(f'Est-ce que vous vous trompez de nombre ? Si oui, {names}, vous pourrez commencer votre jeu ! Sinon, retypez "$spy num_players", svp !')
                
@bot.command()
async def dsv(ctx, num: str,*para):
    if int(ctx.channel.id) != 811359562933338142:
        await ctx.send('Pardon, cette commande ne peut fonctionner que dans le channel [游戏室-JEUX].')
    else:
        if int(num)<=1:
            await ctx.send('Coucou ! Il faut au moins 2 joueurs.')
        else:
            await ctx.send(f'Les joueurs tapent "1" ici, svp !');players=[]
            msg=ctx.message;conn=1;t=time.time()
            while time.time()-t<=t_jeu and conn!=0 : 
                async for message in ctx.channel.history(limit=10,after=msg):
                    if "1" in message.content and message.author not in players and message.author!=bot.user:
                        players.append(message.author)
                    msg=message
                    if len(players)==int(num):
                        conn=0;break
            if len(players)<=1:
                await ctx.send('Coucou ! Il faut au moins 2 joueurs.')
            else:
                n_id=random.sample(range(0,len(dsv_db)),len(players));names=[]
                async for i in range(len(players)):
                    await players[i].send(f'Coucou ! Votre mot: {dsv_db[n_id[i]]}')
                    await players[i].send(f"Vous pouvez utiliser cette lien :　https://r7.whiteboardfox.com/")
                    names.append(players[i].name)
                if len(names)==int(num):
                    await ctx.send(f'Coucou ! {names}, vous pourrez commencer votre jeu !')
                else:
                    await ctx.send(f'Est-ce que vous vous trompez de nombre ? Si oui, {names}, vous pourrez commencer votre jeu ! Sinon, retypez "$dsv num_players", svp !')

@bot.command()
async def id(ctx,*para):
    user=ctx.author
    await user.send(f"Coucou ! Votre ID est : {ctx.author.id}")

@bot.command()
async def info(ctx,*para):
    embed = discord.Embed(title="CC", description=description, color=0xeee657)
    embed.add_field(name="Parent", value="Club Chine Centrale Lyon")
    embed.add_field(name="Date de Naissance", value="21/02/2021", inline=False)
    embed.add_field(name="Sexe", value="À deviner", inline=False)
    embed.add_field(name="Taille", value="150cm&35kg", inline=False)
    embed.add_field(name="Loisirs",value="Cuisine, Télé, Calligraphie, Kongfu, Peinture, Poèmes", inline=False)
    embed.add_field(name="$help", value="CC est polyvalente !", inline=False)
    await ctx.send(embed=embed)

bot.remove_command('help')
@bot.command()
async def help(ctx,*para):
    embed = discord.Embed(title="CC", description=description, color=0xeee657)
    embed.add_field(name="$rule", value="Connaître les règlements de jeux disponibles", inline=False)
    embed.add_field(name="$spy num_players", value="Commencez un jeu de Mot-Espion(num_players=nombre de joueurs)", inline=False)
    embed.add_field(name="$dsv num_players", value="Commencez un jeu de Dessiner-Deviner(num_players=nombre de joueurs)", inline=False)
    embed.add_field(name="$translate phrase", value="Translatez une phrase entre la langue chinoise et la langue française", inline=False)
    embed.add_field(name="$info", value="Connaissez plus CC...", inline=False)
    embed.add_field(name="$CC", value="Parlez avec CC ^w^", inline=False)
    await ctx.send(embed=embed)

bot.run(str(input("TOKEN :\t")))
