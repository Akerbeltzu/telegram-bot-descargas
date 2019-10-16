#!/usr/bin/python
# -*- coding: utf8 -*-
# telegram-bot-descargas: Descargador de archivos para Telegram
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# Modificado para QNAP por: @akerbeltzu
# Requisitos:
# telegram_bot https://pypi.python.org/pypi/python-telegram-bot/
# Bot de Telegram y su token (crear con @BotFather)
# Grupo de Telegram y su CHAT ID


import time
from os import path
import requests

from multiprocessing import Process, Manager
from telegram import Bot, ReplyKeyboardMarkup
from telegram.error import TelegramError


# CONFIGURACIÓN 

# PÁRAMETROS PARA MODIFICAR CON TUS DATOS
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""
DOWNLOADS_FOLDER="/share/Download"

#OTROS DATOS CONFIGURABLES
TELEGRAM_TIMEOUT=50
TELEGRAM_REFRESH_SECONDS=1
# FIN CONFIGURACIÓN

# DOWNLOAD INDEPENDENT PROCESS
def downloader(filenames,urls):
  filename=""
  while filename != "QUIT":
     try:
         filename=filenames.pop(0)
         url=urls.pop(0)
     except IndexError:
         time.sleep(5)

     if filename and filename != "QUIT":
        print("Downloading:"+filename+ ' from '+url)
        r = requests.get(url, stream=True)
        with open(path.join(DOWNLOADS_FOLDER,filename), 'wb') as f:
           for chunk in r.iter_content(chunk_size=1024): 
              if chunk: 
                  f.write(chunk)
        print("Download completed")
        filename=""
 



if __name__ == '__main__':
# START

    bot = Bot(TELEGRAM_BOT_TOKEN)

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Estoy listo, estoy listo!")
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Comparte tus archivos aquí y los enviaré al NAS para ti")

    manager = Manager()
    filenames = manager.list()
    urls = manager.list()
    download_process = Process(target=downloader, args=(filenames,urls,))
    download_process.daemon = True
    download_process.start()

    update_id=0
    user_quit=False

# MAIN LOOP


    while not user_quit:

        try:
            telegram_updates=bot.get_updates(offset=update_id, timeout=TELEGRAM_TIMEOUT)
        except:
            telegram_updates=[]

        for update in telegram_updates:
#            print(update) 
            update_id = update.update_id + 1

    # TEXT MESSAGES
            try:
                user_command=update.message.text
            except AttributeError:
                user_command=None
                pass

            if user_command and user_command.lower() == "quit":
                filenames.append("QUIT")
                download_process.join()
                user_quit=True
                telegram_updates=bot.get_updates(offset=update_id, timeout=TELEGRAM_TIMEOUT) # mark this as read or Telegram will send it again
                break

            elif user_command == "?":
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=str(len(filenames)))
       
    # FILE MESSAGES

            try:
                newfile=update.message.document
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Descargando archivo %s (%i bytes)" %(newfile.file_name, newfile.file_size))
                tfile=bot.getFile(newfile.file_id)
                filenames.append(newfile.file_name)          
                urls.append(tfile.file_path)          
            except AttributeError:
                pass
        
        
                        
        time.sleep(TELEGRAM_REFRESH_SECONDS)



