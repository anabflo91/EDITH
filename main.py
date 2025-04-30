from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import datetime
from flask import Flask
from threading import Thread
from flask import Response
app = Flask('')

@app.route('/', methods=["GET", "HEAD"])
def home():
        html = """
        <html>
            <head><title>Viernes</title></head>
            <body>
                Hola, soy Viernes y estoy despierta
            </body>
        </html>
        """
        return Response(html, mimetype='text/html')

def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
    # --- CONFIGURACIÓN PRINCIPAL ---
TOKEN = "8172080235:AAGmr8CU-jGbE7DXwTQw9-kQB_Rv7TWeNmg"  # Tu token amor
CHAT_ID = None

    # --- CALENDARIO DEL SUPLEMENTO (actualizado) ---
    # Fechas desde 27 abril 2025 hasta 31 diciembre 2025, con ciclos de 6 semanas + 1 de descanso
dias_suplemento = [
        # Abril
        "2025-04-27",
        "2025-04-29",
        # Mayo
        "2025-05-01","2025-05-03","2025-05-05","2025-05-07","2025-05-09","2025-05-11","2025-05-13","2025-05-15","2025-05-17","2025-05-19","2025-05-21","2025-05-23","2025-05-25","2025-05-27","2025-05-29","2025-05-31",
        # Junio
        "2025-06-02","2025-06-04","2025-06-06","2025-06-08","2025-06-10","2025-06-12","2025-06-14",
        # (Descanso del 15 al 21 junio)
        "2025-06-22","2025-06-24","2025-06-26","2025-06-28","2025-06-30",
        # Julio
        "2025-07-02","2025-07-04","2025-07-06","2025-07-08","2025-07-10","2025-07-12","2025-07-14","2025-07-16","2025-07-18","2025-07-20","2025-07-22","2025-07-24","2025-07-26",
        # (Descanso del 27 julio al 2 agosto)
        "2025-08-03","2025-08-05","2025-08-07","2025-08-09","2025-08-11","2025-08-13","2025-08-15","2025-08-17","2025-08-19","2025-08-21","2025-08-23",
        # Septiembre
        "2025-08-25","2025-08-27","2025-08-29","2025-08-31","2025-09-02","2025-09-04","2025-09-06",
        # (Descanso del 7 al 13 septiembre)
        "2025-09-14","2025-09-16","2025-09-18","2025-09-20","2025-09-22","2025-09-24","2025-09-26","2025-09-28","2025-09-30",
        # Octubre
        "2025-10-02","2025-10-04","2025-10-06","2025-10-08","2025-10-10",
        # (Descanso del 11 al 17 octubre)
        "2025-10-18","2025-10-20","2025-10-22","2025-10-24","2025-10-26","2025-10-28","2025-10-30",
        # Noviembre
        "2025-11-01","2025-11-03","2025-11-05","2025-11-07","2025-11-09","2025-11-11",
        # (Descanso del 12 al 18 noviembre)
        "2025-11-19","2025-11-21","2025-11-23","2025-11-25","2025-11-27","2025-11-29",
        # Diciembre
        "2025-12-01","2025-12-03","2025-12-05","2025-12-07","2025-12-09","2025-12-11","2025-12-13","2025-12-15","2025-12-17","2025-12-19","2025-12-21","2025-12-23","2025-12-25","2025-12-27","2025-12-29","2025-12-31"
    ]

    # --- TURNOS DE TRABAJO (sólo ejemplos) ---
    # Aquí debes cargar tu archivo de turnos reales si quieres más adelante
turnos_trabajo = {
    "2025-04-28":"Primero",
    "2025-04-29":"Primero",
    "2025-04-30":"Primero",
    "2025-05-01":"Festivo",
    "2025-05-02":"Primero",
    "2025-05-05":"Tercero",
    "2025-05-06":"Tercero",
    "2025-05-07":"Tercero",
    "2025-05-08":"Tercero",
    "2025-05-09":"Tercero",
    "2025-05-12":"Tercero",
    "2025-05-13":"Tercero",
    "2025-05-14":"Tercero",
    "2025-05-15":"Tercero",
    "2025-05-16":"Tercero",
    "2025-05-19":"Segundo",
    "2025-05-20":"Segundo",
    "2025-05-21":"Segundo",
    "2025-05-22":"Segundo",
    "2025-05-23":"Segundo",
    "2025-05-24":"Segundo",
    "2025-05-26":"Segundo",
    "2025-05-27":"Segundo",
    "2025-05-28":"Segundo",
    "2025-05-29":"Segundo",
    "2025-05-30":"Segundo",
    "2025-05-31":"Segundo",
    "2025-06-02":"Primero",
    "2025-06-03":"Primero",
    "2025-06-04":"Primero",
    "2025-06-05":"Primero",
    "2025-06-06":"Primero",
    "2025-06-09":"Primero",
    "2025-06-10":"Primero",
    "2025-06-11":"Primero",
    "2025-06-12":"Primero",
    "2025-06-13":"Primero",
    "2025-06-16":"Tercero",
    "2025-06-17":"Tercero",
    "2025-06-18":"Tercero",
    "2025-06-19":"Tercero",
    "2025-06-20":"Tercero",
    "2025-06-23":"Tercero",
    "2025-06-24":"Tercero",
    "2025-06-25":"Tercero",
    "2025-06-26":"Tercero",
    "2025-06-27":"Tercero",
    "2025-06-30":"Segundo",
    "2025-07-01":"Segundo",
    "2025-07-02":"Segundo",
    "2025-07-03":"Segundo",
    "2025-07-04":"Segundo",
    "2025-07-05":"Segundo",
    "2025-07-07":"Segundo",
    "2025-07-08":"Segundo",
    "2025-07-09":"Segundo",
    "2025-07-10":"Segundo",
    "2025-07-11":"Segundo",
    "2025-07-12":"Segundo",
    "2025-07-14":"Primero",
    "2025-07-15":"Primero",
    "2025-07-16":"Primero",
    "2025-07-17":"Primero",
    "2025-07-18":"Primero",
    "2025-07-21":"Primero",
    "2025-07-22":"Primero",
    "2025-07-23":"Primero",
    "2025-07-24":"Primero",
    "2025-07-25":"Primero",
    "2025-07-28":"Tercero",
    "2025-07-29":"Tercero",
    "2025-07-30":"Tercero",
    "2025-07-31":"Tercero",
    "2025-08-01":"Tercero",
    "2025-08-04":"Tercero",
    "2025-08-05":"Tercero",
    "2025-08-06":"Tercero",
    "2025-08-07":"Tercero",
    "2025-08-08":"Tercero",
    "2025-08-11":"Segundo",
    "2025-08-12":"Segundo",
    "2025-08-13":"Segundo",
    "2025-08-14":"Segundo",
    "2025-08-15":"Segundo",
    "2025-08-16":"Segundo",
    "2025-08-18":"Segundo",
    "2025-08-19":"Segundo",
    "2025-08-20":"Segundo",
    "2025-08-21":"Segundo",
    "2025-08-22":"Segundo",
    "2025-08-23":"Segundo",
    "2025-08-25":"Primero",
    "2025-08-26":"Primero",
    "2025-08-27":"Primero",
    "2025-08-28":"Primero",
    "2025-08-29":"Primero",
    "2025-09-01":"Primero",
    "2025-09-02":"Primero",
    "2025-09-03":"Primero",
    "2025-09-04":"Primero",
    "2025-09-05":"Primero",
    "2025-09-08":"Tercero",
    "2025-09-09":"Tercero",
    "2025-09-10":"Tercero",
    "2025-09-11":"Tercero",
    "2025-09-12":"Tercero",
    "2025-09-15":"Tercero",
    "2025-09-16":"Festivo",
    "2025-09-17":"Tercero",
    "2025-09-18":"Tercero",
    "2025-09-19":"Tercero",
    "2025-09-22":"Segundo",
    "2025-09-23":"Segundo",
    "2025-09-24":"Segundo",
    "2025-09-25":"Segundo",
    "2025-09-26":"Segundo",
    "2025-09-27":"Segundo",
    "2025-09-29":"Segundo",
    "2025-09-30":"Segundo",
    "2025-10-01":"Segundo",
    "2025-10-02":"Segundo",
    "2025-10-03":"Segundo",
    "2025-10-04":"Segundo",
    "2025-10-06":"Primero",
    "2025-10-07":"Primero",
    "2025-10-08":"Primero",
    "2025-10-09":"Primero",
    "2025-10-10":"Primero",
    "2025-10-13":"Primero",
    "2025-10-14":"Primero",
    "2025-10-15":"Primero",
    "2025-10-16":"Primero",
    "2025-10-17":"Primero",
    "2025-10-20":"Tercero",
    "2025-10-21":"Tercero",
    "2025-10-22":"Tercero",
    "2025-10-23":"Tercero",
    "2025-10-24":"Tercero",
    "2025-10-27":"Tercero",
    "2025-10-28":"Tercero",
    "2025-10-29":"Tercero",
    "2025-10-30":"Tercero",
    "2025-10-31":"Tercero",
    "2025-11-03":"Segundo",
    "2025-11-04":"Segundo",
    "2025-11-05":"Segundo",
    "2025-11-06":"Segundo",
    "2025-11-07":"Segundo",
    "2025-11-08":"Segundo",
    "2025-11-10":"Segundo",
    "2025-11-11":"Segundo",
    "2025-11-12":"Segundo",
    "2025-11-13":"Segundo",
    "2025-11-14":"Segundo",
    "2025-11-15":"Segundo",
    "2025-11-17":"Festivo",
    "2025-11-18":"Primero",
    "2025-11-19":"Primero",
    "2025-11-20":"Primero",
    "2025-11-21":"Primero",
    "2025-11-24":"Primero",
    "2025-11-25":"Primero",
    "2025-11-26":"Primero",
    "2025-11-27":"Primero",
    "2025-11-28":"Primero",
    "2025-12-01":"Tercero",
    "2025-12-02":"Tercero",
    "2025-12-03":"Tercero",
    "2025-12-04":"Tercero",
    "2025-12-05":"Tercero",
    "2025-12-08":"Tercero",
    "2025-12-09":"Tercero",
    "2025-12-10":"Tercero",
    "2025-12-11":"Tercero",
    "2025-12-12":"Tercero",
    "2025-12-15":"Segundo",
    "2025-12-16":"Segundo",
    "2025-12-17":"Segundo",
    "2025-12-18":"Segundo",
    "2025-12-19":"Segundo",
    "2025-12-20":"Segundo",
    "2025-12-22":"Segundo",
    "2025-12-23":"Segundo",
    "2025-12-24":"Segundo",
    "2025-12-25":"Festivo",
    "2025-12-26":"Segundo",
    "2025-12-27":"Segundo",
    "2025-12-29":"Primero",
    "2025-12-30":"Primero",
    "2025-12-31":"Primero",

    
        # Puedes seguir llenando según tu calendario real
    }

    # --- FUNCIONES DEL BOT ---

def recordatorio_suplemento(context):
        hoy = datetime.datetime.now(timezone('America/Mexico_City')).strftime('%Y-%m-%d')
        if CHAT_ID:
         if hoy in dias_suplemento:
            context.bot.send_message(chat_id=CHAT_ID, text="Buenos días, es hora de tomar tu suplemento.")
        else:
            context.bot.send_message(chat_id=CHAT_ID, text="Hoy no toca suplemento.")

def mensaje_buenas_noches(context):
        ahora = datetime.datetime.now(timezone('America/Mexico_City'))
        if CHAT_ID:
             context.bot.send_message(chat_id=CHAT_ID, text="Buenas noches, guarda tu suplemento para mañana.")
            

def turno_consulta(update, context):
        global CHAT_ID
        CHAT_ID = update.effective_chat.id
        mensaje = update.message.text.lower()
        if "turno para el" in mensaje:
            try:
                partes = mensaje.split("turno para el")[1].strip().split()
                dia = int(partes[0])
                mes_nombre = partes[1].lower()
                meses = {
                    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
                    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
                    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
                }
                mes = meses[mes_nombre]
                fecha = datetime.date(2025, mes, dia).strftime("%Y-%m-%d")
                turno = turnos_trabajo.get(fecha)
                if turno:
                    update.message.reply_text(f"El {dia} de {mes_nombre} tienes turno {turno}.")
                else:
                    update.message.reply_text("Dia de descanso, sábado o domingo.")
            except Exception as e:
                update.message.reply_text("No entendí la fecha.")

def start(update, context):
        global CHAT_ID
        CHAT_ID = update.effective_chat.id
        update.message.reply_text("¡Hola, Soy Viernes. Estoy aquí para asistirte. Pregúntame tu turno o espera mis recordatorios.")

# ---------------------- INICIO BLOQUE POKA-YOKE SUPLEMENTO ----------------------

historial_suplemento = {}

def tomado(update, context):
    hoy = datetime.datetime.now(timezone('America/Mexico_City')).strftime('%Y-%m-%d')
    historial_suplemento[hoy] = 'Tomado'
    context.bot.send_message(chat_id=update.effective_chat.id, text="✨ Suplemento registrado como TOMADO hoy.")

def omitido(update, context):
    hoy = datetime.datetime.now(timezone('America/Mexico_City')).strftime('%Y-%m-%d')
    historial_suplemento[hoy] = 'Omitido'
    context.bot.send_message(chat_id=update.effective_chat.id, text="😥 Suplemento registrado como OMITIDO hoy.")

def historial(update, context):
    if not historial_suplemento:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Aún no hay historial registrado.")
        return
    texto = "📆 Historial de suplemento:\n"
    for fecha, estado in sorted(historial_suplemento.items()):
        texto += f"{fecha}: {estado}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=texto)

# ---------------------- FIN BLOQUE POKA-YOKE SUPLEMENTO ----------------------

def main():
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, turno_consulta))
        dp.add_handler(CommandHandler("tomado", tomado))
        dp.add_handler(CommandHandler("omitido", omitido))
        dp.add_handler(CommandHandler("historial", historial))
        scheduler = BackgroundScheduler(timezone=timezone('America/Mexico_City'))
        scheduler.add_job(recordatorio_suplemento, 'cron', hour=10, minute=0, args=[updater.job_queue])
        scheduler.add_job(mensaje_buenas_noches, 'cron', hour=21, minute=0, args=[updater.job_queue])
        scheduler.start()
        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
        keep_alive()
        main()
