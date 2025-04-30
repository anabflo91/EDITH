import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz

import os
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

zona = pytz.timezone("America/Mexico_City")

# ---------------- POKA-YOKE ----------------
estado_dosis = {}

@bot.command()
async def tomado(ctx):
    hoy = datetime.now(zona).strftime("%Y-%m-%d")
    estado_dosis[hoy] = "Tomado"
    await ctx.send(f"✅ Suplemento marcado como **tomado** para hoy ({hoy})")

@bot.command()
async def omitido(ctx):
    hoy = datetime.now(zona).strftime("%Y-%m-%d")
    estado_dosis[hoy] = "Omitido"
    await ctx.send(f"⚠️ Suplemento marcado como **omitido** para hoy ({hoy})")

@bot.command()
async def historial(ctx):
    if not estado_dosis:
        await ctx.send("Aún no hay historial registrado.")
    else:
        mensaje = "**  Historial de dosis:**\n"
        for fecha, estado in sorted(estado_dosis.items()):
            mensaje += f"- {fecha}: {estado}\n"
        await ctx.send(mensaje)

# ---------------- SUPLEMENTO ----------------
inicio_suplemento = datetime(2024, 4, 27)

@bot.command()
async def suplemento(ctx, fecha: str = None):
    hoy = datetime.now(zona) if not fecha else datetime.strptime(fecha, "%Y-%m-%d")
    dias_transcurridos = (hoy - inicio_suplemento).days
    ciclo = (dias_transcurridos // 14) + 1
    dia_en_ciclo = dias_transcurridos % 14

    if 7 <= dia_en_ciclo <= 13:
        await ctx.send(f"  El {hoy.strftime('%Y-%m-%d')} corresponde a la semana de **descanso** del ciclo {ciclo}.")
    else:
        await ctx.send(f"  El {hoy.strftime('%Y-%m-%d')} corresponde a la semana de **toma** del suplemento en el ciclo {ciclo}.")

# ---------------- TURNOS ----------------
turnos_registrados = {
    "2025-04-27": "Domingo",
    "2025-04-28": "Turno 1 (Mañana)",
    "2025-04-29": "Turno 1 (Mañana)",
    "2025-04-30": "Turno 1 (Mañana)",
    "2025-05-01": "Turno 1 (Mañana)",
    "2025-05-02": "Turno 1 (Mañana)",
    "2025-05-03": "Sábado (Descanso)",
    "2025-05-04": "Domingo",
    "2025-05-05": "Turno 3 (Noche)",
    "2025-05-06": "Turno 3 (Noche)",
    "2025-05-07": "Turno 3 (Noche)",
    "2025-05-08": "Turno 3 (Noche)",
    "2025-05-09": "Turno 3 (Noche)",
    "2025-05-10": "Turno 3 (Noche - Sábado)",
    "2025-05-11": "Domingo",
    "2025-05-12": "Turno 2 (Tarde)",
    "2025-05-13": "Turno 2 (Tarde)",
    "2025-05-14": "Turno 2 (Tarde)",
    "2025-05-15": "Turno 2 (Tarde)",
    "2025-05-16": "Turno 2 (Tarde)",
    "2025-05-17": "Turno 1 (Mañana)",
    "2025-05-18": "Domingo",
    "2025-05-19": "Turno 1 (Mañana)",
    "2025-05-20": "Turno 1 (Mañana)",
    "2025-05-21": "Turno 1 (Mañana)",
    "2025-05-22": "Turno 1 (Mañana)",
    "2025-05-23": "Turno 1 (Mañana)",
    "2025-05-24": "Sábado (Descanso)",
    "2025-05-25": "Domingo",
    "2025-05-26": "Turno 3 (Noche)",
    "2025-05-27": "Turno 3 (Noche)",
    "2025-05-28": "Turno 3 (Noche)",
    "2025-05-29": "Turno 3 (Noche)",
    "2025-05-30": "Turno 3 (Noche)",
    "2025-05-31": "Turno 3 (Noche - Sábado)",
    "2025-06-01": "Domingo",
    "2025-06-02": "Turno 2 (Tarde)",
    "2025-06-03": "Turno 2 (Tarde)",
    "2025-06-04": "Turno 2 (Tarde)",
    "2025-06-05": "Turno 2 (Tarde)",
    "2025-06-06": "Turno 2 (Tarde)",
    "2025-06-07": "Turno 1 (Mañana)",
    "2025-06-08": "Domingo",
    "2025-06-09": "Turno 1 (Mañana)",
    "2025-06-10": "Turno 1 (Mañana)",
    "2025-06-11": "Turno 1 (Mañana)",
    "2025-06-12": "Turno 1 (Mañana)",
    "2025-06-13": "Turno 1 (Mañana)",
    "2025-06-14": "Sábado (Descanso)",
    "2025-06-15": "Domingo",
    "2025-06-16": "Turno 3 (Noche)",
    "2025-06-17": "Turno 3 (Noche)",
    "2025-06-18": "Turno 3 (Noche)",
    "2025-06-19": "Turno 3 (Noche)",
    "2025-06-20": "Turno 3 (Noche)",
    "2025-06-21": "Turno 3 (Noche - Sábado)",
    "2025-06-22": "Domingo",
    "2025-06-23": "Turno 2 (Tarde)",
    "2025-06-24": "Turno 2 (Tarde)",
    "2025-06-25": "Turno 2 (Tarde)",
    "2025-06-26": "Turno 2 (Tarde)",
    "2025-06-27": "Turno 2 (Tarde)",
    "2025-06-28": "Turno 1 (Mañana)",
    "2025-06-29": "Domingo",
    "2025-06-30": "Turno 1 (Mañana)",
    "2025-07-01": "Turno 1 (Mañana)",
    "2025-07-02": "Turno 1 (Mañana)",
    "2025-07-03": "Turno 1 (Mañana)",
    "2025-07-04": "Turno 1 (Mañana)",
    "2025-07-05": "Sábado (Descanso)",
    "2025-07-06": "Domingo",
    "2025-07-07": "Turno 3 (Noche)",
    "2025-07-08": "Turno 3 (Noche)",
    "2025-07-09": "Turno 3 (Noche)",
    "2025-07-10": "Turno 3 (Noche)",
    "2025-07-11": "Turno 3 (Noche)",
    "2025-07-12": "Turno 3 (Noche - Sábado)",
    "2025-07-13": "Domingo",
    "2025-07-14": "Turno 2 (Tarde)",
    "2025-07-15": "Turno 2 (Tarde)",
    "2025-07-16": "Turno 2 (Tarde)",
    "2025-07-17": "Turno 2 (Tarde)",
    "2025-07-18": "Turno 2 (Tarde)",
    "2025-07-19": "Turno 1 (Mañana)",
    "2025-07-20": "Domingo",
    "2025-07-21": "Turno 1 (Mañana)",
    "2025-07-22": "Turno 1 (Mañana)",
    "2025-07-23": "Turno 1 (Mañana)",
    "2025-07-24": "Turno 1 (Mañana)",
    "2025-07-25": "Turno 1 (Mañana)",
    "2025-07-26": "Sábado (Descanso)",
    "2025-07-27": "Domingo",
    "2025-07-28": "Turno 3 (Noche)",
    "2025-07-29": "Turno 3 (Noche)",
    "2025-07-30": "Turno 3 (Noche)",
    "2025-07-31": "Turno 3 (Noche)",
    "2025-08-01": "Turno 3 (Noche)",
    "2025-08-02": "Turno 3 (Noche - Sábado)",
    "2025-08-03": "Domingo",
    "2025-08-04": "Turno 2 (Tarde)",
    "2025-08-05": "Turno 2 (Tarde)",
    "2025-08-06": "Turno 2 (Tarde)",
    "2025-08-07": "Turno 2 (Tarde)",
    "2025-08-08": "Turno 2 (Tarde)",
    "2025-08-09": "Turno 1 (Mañana)",
    "2025-08-10": "Domingo",
    "2025-08-11": "Turno 1 (Mañana)",
    "2025-08-12": "Turno 1 (Mañana)",
    "2025-08-13": "Turno 1 (Mañana)",
    "2025-08-14": "Turno 1 (Mañana)",
    "2025-08-15": "Turno 1 (Mañana)",
    "2025-08-16": "Sábado (Descanso)",
    "2025-08-17": "Domingo",
    "2025-08-18": "Turno 3 (Noche)",
    "2025-08-19": "Turno 3 (Noche)",
    "2025-08-20": "Turno 3 (Noche)",
    "2025-08-21": "Turno 3 (Noche)",
    "2025-08-22": "Turno 3 (Noche)",
    "2025-08-23": "Turno 3 (Noche - Sábado)",
    "2025-08-24": "Domingo",
    "2025-08-25": "Turno 2 (Tarde)",
    "2025-08-26": "Turno 2 (Tarde)",
    "2025-08-27": "Turno 2 (Tarde)",
    "2025-08-28": "Turno 2 (Tarde)",
    "2025-08-29": "Turno 2 (Tarde)",
    "2025-08-30": "Turno 1 (Mañana)",
    "2025-08-31": "Domingo",
    "2025-09-01": "Turno 1 (Mañana)",
    "2025-09-02": "Turno 1 (Mañana)",
    "2025-09-03": "Turno 1 (Mañana)",
    "2025-09-04": "Turno 1 (Mañana)",
    "2025-09-05": "Turno 1 (Mañana)",
    "2025-09-06": "Sábado (Descanso)",
    "2025-09-07": "Domingo",
    "2025-09-08": "Turno 3 (Noche)",
    "2025-09-09": "Turno 3 (Noche)",
    "2025-09-10": "Turno 3 (Noche)",
    "2025-09-11": "Turno 3 (Noche)",
    "2025-09-12": "Turno 3 (Noche)",
    "2025-09-13": "Turno 3 (Noche - Sábado)",
    "2025-09-14": "Domingo",
    "2025-09-15": "Turno 2 (Tarde)",
    "2025-09-16": "Turno 2 (Tarde)",
    "2025-09-17": "Turno 2 (Tarde)",
    "2025-09-18": "Turno 2 (Tarde)",
    "2025-09-19": "Turno 2 (Tarde)",
    "2025-09-20": "Turno 1 (Mañana)",
    "2025-09-21": "Domingo",
    "2025-09-22": "Turno 1 (Mañana)",
    "2025-09-23": "Turno 1 (Mañana)",
    "2025-09-24": "Turno 1 (Mañana)",
    "2025-09-25": "Turno 1 (Mañana)",
    "2025-09-26": "Turno 1 (Mañana)",
    "2025-09-27": "Sábado (Descanso)",
    "2025-09-28": "Domingo",
    "2025-09-29": "Turno 3 (Noche)",
    "2025-09-30": "Turno 3 (Noche)",
    "2025-10-01": "Turno 3 (Noche)",
    "2025-10-02": "Turno 3 (Noche)",
    "2025-10-03": "Turno 3 (Noche)",
    "2025-10-04": "Turno 3 (Noche - Sábado)",
    "2025-10-05": "Domingo",
    "2025-10-06": "Turno 2 (Tarde)",
    "2025-10-07": "Turno 2 (Tarde)",
    "2025-10-08": "Turno 2 (Tarde)",
    "2025-10-09": "Turno 2 (Tarde)",
    "2025-10-10": "Turno 2 (Tarde)",
    "2025-10-11": "Turno 1 (Mañana)",
    "2025-10-12": "Domingo",
    "2025-10-13": "Turno 1 (Mañana)",
    "2025-10-14": "Turno 1 (Mañana)",
    "2025-10-15": "Turno 1 (Mañana)",
    "2025-10-16": "Turno 1 (Mañana)",
    "2025-10-17": "Turno 1 (Mañana)",
    "2025-10-18": "Sábado (Descanso)",
    "2025-10-19": "Domingo",
    "2025-10-20": "Turno 3 (Noche)",
    "2025-10-21": "Turno 3 (Noche)",
    "2025-10-22": "Turno 3 (Noche)",
    "2025-10-23": "Turno 3 (Noche)",
    "2025-10-24": "Turno 3 (Noche)",
    "2025-10-25": "Turno 3 (Noche - Sábado)",
    "2025-10-26": "Domingo",
    "2025-10-27": "Turno 2 (Tarde)",
    "2025-10-28": "Turno 2 (Tarde)",
    "2025-10-29": "Turno 2 (Tarde)",
    "2025-10-30": "Turno 2 (Tarde)",
    "2025-10-31": "Turno 2 (Tarde)",
    "2025-11-01": "Turno 1 (Mañana)",
    "2025-11-02": "Domingo",
    "2025-11-03": "Turno 1 (Mañana)",
    "2025-11-04": "Turno 1 (Mañana)",
    "2025-11-05": "Turno 1 (Mañana)",
    "2025-11-06": "Turno 1 (Mañana)",
    "2025-11-07": "Turno 1 (Mañana)",
    "2025-11-08": "Sábado (Descanso)",
    "2025-11-09": "Domingo",
    "2025-11-10": "Turno 3 (Noche)",
    "2025-11-11": "Turno 3 (Noche)",
    "2025-11-12": "Turno 3 (Noche)",
    "2025-11-13": "Turno 3 (Noche)",
    "2025-11-14": "Turno 3 (Noche)",
    "2025-11-15": "Turno 3 (Noche - Sábado)",
    "2025-11-16": "Domingo",
    "2025-11-17": "Turno 2 (Tarde)",
    "2025-11-18": "Turno 2 (Tarde)",
    "2025-11-19": "Turno 2 (Tarde)",
    "2025-11-20": "Turno 2 (Tarde)",
    "2025-11-21": "Turno 2 (Tarde)",
    "2025-11-22": "Turno 1 (Mañana)",
    "2025-11-23": "Domingo",
    "2025-11-24": "Turno 1 (Mañana)",
    "2025-11-25": "Turno 1 (Mañana)",
    "2025-11-26": "Turno 1 (Mañana)",
    "2025-11-27": "Turno 1 (Mañana)",
    "2025-11-28": "Turno 1 (Mañana)",
    "2025-11-29": "Sábado (Descanso)",
    "2025-11-30": "Domingo",
    "2025-12-01": "Turno 3 (Noche)",
    "2025-12-02": "Turno 3 (Noche)",
    "2025-12-03": "Turno 3 (Noche)",
    "2025-12-04": "Turno 3 (Noche)",
    "2025-12-05": "Turno 3 (Noche)",
    "2025-12-06": "Turno 3 (Noche - Sábado)",
    "2025-12-07": "Domingo",
    "2025-12-08": "Turno 2 (Tarde)",
    "2025-12-09": "Turno 2 (Tarde)",
    "2025-12-10": "Turno 2 (Tarde)",
    "2025-12-11": "Turno 2 (Tarde)",
    "2025-12-12": "Turno 2 (Tarde)",
    "2025-12-13": "Turno 1 (Mañana)",
    "2025-12-14": "Domingo",
    "2025-12-15": "Turno 1 (Mañana)",
    "2025-12-16": "Turno 1 (Mañana)",
    "2025-12-17": "Turno 1 (Mañana)",
    "2025-12-18": "Turno 1 (Mañana)",
    "2025-12-19": "Turno 1 (Mañana)",
    "2025-12-20": "Sábado (Descanso)",
    "2025-12-21": "Domingo",
    "2025-12-22": "Turno 3 (Noche)",
    "2025-12-23": "Turno 3 (Noche)",
    "2025-12-24": "Turno 3 (Noche)",
    "2025-12-25": "Turno 3 (Noche)",
    "2025-12-26": "Turno 3 (Noche)",
    "2025-12-27": "Turno 3 (Noche - Sábado)",
    "2025-12-28": "Domingo",
    "2025-12-29": "Turno 2 (Tarde)",
    "2025-12-30": "Turno 2 (Tarde)",
    "2025-12-31": "Turno 2 (Tarde)",
    "2026-01-01": "Turno 2 (Tarde)",

}

@bot.command()
async def turno(ctx, fecha: str = None):
    if fecha:
        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            await ctx.send("❌ Formato incorrecto. Usa: `/turno YYYY-MM-DD`")
            return
    else:
        fecha_dt = datetime.now(zona).date()

    fecha_str = fecha_dt.strftime("%Y-%m-%d")
    if fecha_str in turnos_registrados:
        resultado = turnos_registrados[fecha_str]
        await ctx.send(f"  El día {fecha_str} corresponde a: **{resultado}**")
    else:
        await ctx.send(f"  El día {fecha_str} no tiene turno registrado.")

# ---------------- INICIO ----------------
@bot.command()
async def start(ctx):
    mensaje = (
        "**¡Hola! Soy E.D.I.T.H. tu asistente personal.**  \n"
        "Estos son los comandos disponibles:\n"
        "  `/turno [YYYY-MM-DD]` → Consulta tu turno.\n"
        "  `/suplemento [YYYY-MM-DD]` → Consulta si tomas o descansas suplemento.\n"
        "  `/tomado` → Marcar suplemento como tomado hoy.\n"
        "  `/omitido` → Marcar suplemento como omitido hoy.\n"
        "  `/historial` → Ver historial de suplementación."
    )
    await ctx.send(mensaje)


bot.run(os.getenv("TOKEN"))
