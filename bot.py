# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json

#res.json es un archivo json donde guardo el token del bot e IDs importantes
with open('res.json') as json_file:
    data = json.load(json_file)
bot = telebot.TeleBot(data['Token'])

# Ids importantes
administrador = int(data['Administrador'])

#groups.txt lo uso para guardar los IDs de grupos donde se usa el bot para en caso de necesitar enviar informacion a los usuarios TODO: Comando para enviar msj a los grupos
grupos = [line.rstrip('\n') for line in open('grupos.txt')]

def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            if cid > 0 and cid != administrador:   
                bot.send_message(cid, "Este bot solo puede ser utilizado en grupos.")
            elif cid < 0:
                if not str(cid) in grupos:
                    grupos.append(str(cid))
                    aux = open( 'grupos.txt', 'a')
                    aux.write(str(cid) + "\n")
                    aux.close()
                    f = open(f"{cid}.txt", "x")
                    f.close()
                try:
                    f = open(f'{cid}.txt', 'r')
                    content = f.read()
                    if str(m.from_user.id) in content:
                        f.close()
                    else:
                        f.close()
                        f = open(f'{cid}.txt', 'a')
                        f.write(f"[{m.from_user.first_name}](tg://user?id={m.from_user.id}) ")
                        f.close()
                except:
                    bot.send_message(administrador, f"Error al guardar\nGrupo: {cid}\nID usuario: {m.from_user.id}")

bot.set_update_listener(listener)

@bot.message_handler(func=lambda message: message.text == '/invocar' or '@everyone' in message.text or message.text == '/invocar@invocacion_bot')
def comando_invocar(m):
    cid = m.chat.id
    if cid < 0:
            f = open(f'{cid}.txt', 'r')
            bot.send_message(cid, f.read(), parse_mode='Markdown')
            f.close()

			
bot.polling(none_stop=True)