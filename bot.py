import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قاموس لتخزين النقاط وترتيب اللاعبين مؤقتاً
player_scores = {}

@bot.event
async def on_ready():
    print(f"البوت جاهز شغال باسم: {bot.user}")

@bot.command(name="match")
@commands.has_permissions(administrator=True) # مخصص للحكام أو المشرفين فقط
async def match(ctx, winner: discord.Member, loser: discord.Member, score: str):
    # تحديث النقاط أو تسجيل الفوز
    player_scores[winner.display_name] = player_scores.get(winner.display_name, 0) + 10
    
    # ترتيب اللاعبين من الأعلى للأقل نقاطاً
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    
    # بناء رسالة الإعلان والمباركة
    embed = discord.Embed(
        title="🔥 نتيجة تحدي رسمية في Clan STR 🔥",
        color=discord.Color.gold()
    )
    embed.add_field(name="🏆 الفائز", value=winner.mention, inline=True)
    embed.add_field(name="⚔️ الخاسر", value=loser.mention, inline=True)
    embed.add_field(name="📊 النتيجة", value=score, inline=False)
    
    # بناء قائمة الترتيب (من 1 إلى 50 كحد أقصى)
    leaderboard_text = ""
    for index, (p_name, p_score) in enumerate(sorted_players[:50], start=1):
        medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"#{index}"
        leaderboard_text += f"{medal} **{p_name}** — {p_score} نقطة\n"
    
    if leaderboard_text:
        embed.add_field(name="👑 جدول الصدارة المحدث (توب 50)", value=leaderboard_text, inline=False)
    
    embed.set_footer(text="أداء أسطوري! استمروا في القمة يا أبطال Clan STR ⚡")
    
    await ctx.send(embed=embed)

# التوكن الخاص بك مضاف هنا
bot.run("MTU1MDI0MzE1ODMyNjEyMDQ2OQ.GUHD41.bI0CuLVhxvLTy87WcrwedGCiA907MtiRN5J2YQ")
