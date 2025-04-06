import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
from keep_alive import keep_alive

# .env 파일에서 환경 변수 로드
load_dotenv()

# 봇 토큰 가져오기
TOKEN = os.getenv("DISCORD_TOKEN")

# 봇 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"{bot.user} 로 로그인했습니다!")
    try:
        # 슬래시 명령어 동기화
        synced = await tree.sync()
        print(f"Slash command {len(synced)}개를 동기화했어요.")
    except discord.errors.HTTPException as e:
        print(f"명령어 동기화 오류: {e}")

# 🔥 /불판교체 - 최근 내가 보낸 메시지 N개 삭제
@tree.command(name="불판교체", description="최근 내가 보낸 메시지를 지정한 개수만큼 삭제합니다.")
@app_commands.describe(개수="삭제할 메시지 수")
async def 불판교체(interaction: discord.Interaction, 개수: int):
    await interaction.response.defer(ephemeral=True)
    deleted = 0

    # 메시지 삭제 시 한 번에 너무 많은 메시지를 삭제하지 않도록 10개씩 삭제
    async for message in interaction.channel.history(limit=200):
        if message.author == interaction.user:
            await message.delete()
            deleted += 1
            if deleted >= 개수:
                break
            if deleted % 10 == 0:  # 한 번에 최대 10개씩 삭제
                await asyncio.sleep(1)  # 부하를 줄이기 위해 1초 대기

    await interaction.followup.send(f"✅ 최근 내가 보낸 메시지 {deleted}개를 삭제했어요!", ephemeral=True)

# 🔥 /불판모두교체 - 최근 내가 보낸 모든 메시지 삭제 (최대 100개까지만 삭제)
@tree.command(name="불판모두교체", description="최근 내가 보낸 메시지를 최대 100개까지 삭제합니다.")
async def 불판모두교체(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    deleted = 0

    # 최대 100개까지만 삭제
    async for message in interaction.channel.history(limit=200):
        if message.author == interaction.user:
            await message.delete()
            deleted += 1
            if deleted >= 100:  # 최대 100개까지만 삭제
                break
            if deleted % 10 == 0:  # 한 번에 최대 10개씩 삭제
                await asyncio.sleep(1)  # 부하를 줄이기 위해 1초 대기

    await interaction.followup.send(f"✅ 최근 내가 보낸 메시지 {deleted}개를 모두 삭제했어요!", ephemeral=True)

# Flask 서버 실행 (Replit에서 24/7 봇 실행을 위한 설정)
keep_alive()

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"봇 실행 중 오류 발생: {e}")
