import discord, asyncio
from discord.ext import commands
import youtube_dl
import os
import re
 
app = commands.Bot(command_prefix='!')
iconurl = "https://tumblbug-upi.imgix.net/0c7daa777c44a9daf0fc99bcb9ed394df1c8ca3d.png?ixlib=rb-1.1.0&w=200&h=200&auto=format%2Ccompress&fit=facearea&facepad=2.0&ch=Save-Data&mask=ellipse&s=317083b67ed3cb9ca27d586cd35faeb8"

@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def 실험(ctx, *, text):
    await ctx.send(text)

@app.command()
async def 온라인(ctx):
    await ctx.send('봇이 온라인을 합니다')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def 오프라인(ctx):
    await ctx.send('봇이 로그아웃을 합니다')
    await app.change_presence(status=discord.Status.offline, activity=None)

@app.command()
async def 안녕(ctx):
    id = ctx.author.name
    await ctx.send(str(id)+'님 안녕하세요.')

#음악봇


@app.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel: # 채널에 들어가 있는지 파악
        embed = discord.Embed(title="봇이 음성채널에 입장을 하였습니다.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)
        channel = ctx.author.voice.channel # 채널 구하기
        await channel.connect() # 채널 연결
    else: # 유저가 채널에 없으면
        await ctx.send("채널에 연결되지 않았습니다.")

@app.command(pass_context=True)
async def leave(ctx):
    try:
        if ctx.author.voice.channel == app.voice_clients[0].channel:
            embed = discord.Embed(title="봇이 음성채널에서 퇴장하였습니다.",color=0x9DE4FF)
            embed.set_author(name="소녀봇")
            embed.set_thumbnail(url=iconurl)
            await ctx.send(embed=embed)
            await app.voice_clients[0].disconnect()
        else:
            await ctx.send("봇이랑 같은 음성채널에 들어가 있지 않습니다.")
    except:
        await ctx.send("봇이 음성채널에 들어가 있지 않습니다.")

@app.command()
async def pause(ctx):
    voice = discord.utils.get(app.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        embed = discord.Embed(title="현재 재생중인 음악을 일시정지하였습니다.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("재생중인 음악이 없습니다.")

@app.command()
async def resume(ctx):
    voice = discord.utils.get(app.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        embed = discord.Embed(title="현재 일지중지중인 음악을 다시 재생하였습니다.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("일지정지중인 음악이 업습니다.")

@app.command()
async def stop(ctx):
    voice = discord.utils.get(app.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        embed = discord.Embed(title="현재 재생중인 음악을 정지하였습니다.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("음악이 재생중이지 않습니다.")


@app.command()
async def play(ctx, url : str):
    if ctx.author.voice and ctx.author.voice.channel:
        song_there = os.path.isfile("main.mp3")
        try:
            url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url)
            if url1 == None:
                await ctx.send("올바른 url을 입력해주세요.")
                return
        except IndexError:
                await ctx.send("url를 입력해주세요.")
                return
        
        try:
             if song_there:
                os.remove("main.mp3")
        except PermissionError:
            await ctx.send("현재 재생 중인 음악이 끝날 때까지 기다리거나 'stop' 명령어를 사용해주세요.")
            return

        if ctx.author.voice.channel != app.voice_clients[0].channel:
            await app.voice_clients[0].disconnect()
            voiceChannel = ctx.author.voice.channel
            await voiceChannel.connect()

        voice = discord.utils.get(app.voice_clients,guild=ctx.guild)
        ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192',
            }],
        }

        embed = discord.Embed(title="음악을 다운받는중입니다. 잠시만 기다려 주세요.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url,download=False)
            title = info["title"]
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "main.mp3")
        voice.play(discord.FFmpegPCMAudio("main.mp3",options=f'-af "volume={0.5}"'))

        embed = discord.Embed(title=title+"을 재생합니다.",color=0x9DE4FF)
        embed.set_author(name="소녀봇")
        embed.set_thumbnail(url=iconurl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("채널에 연결되지 않았습니다.")

#음악봇

app.run(os.environ['token'])

