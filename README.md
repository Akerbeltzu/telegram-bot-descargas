# telegram-bot-descargas
Bot de Telegram para descargas de archivos

Si tienes un servidor o un NAS conectado a Internet, y quieres automatizar descargas a una carpeta de tu elección, este es tu bot.

Solo tienes que crear un nuevo bot de Telegram (https://core.telegram.org/bots), y cambiar estas líneas del script

* TELEGRAM_BOT_TOKEN: el TOKEN que identifica a tu bot 
* TELEGRAM_CHAT_ID: el id de tu grupo de Telegram. Si no lo conoces, habla con el bot @get_id_bot y envíale el comando /my_id   
* DOWNLOADS_FOLDER: Cambia la ruta de tu directorio a tu elección.

Instala la librería telegram-bot de python, de Gihub (https://github.com/python-telegram-bot/python-telegram-bot) 

o con el comando pip ( https://pypi.python.org/pypi/python-telegram-bot/).

El módulo "request" también es necesario. Es muy popular y probablemente lo tengas instalado. Si no es así, usa pip.

Ejecuta tu script y envíale archivos!

Con este bot, puedes:

* Enviar un archivo o reenviar de otro grupo a tu grupo y el bot lo descargará a la carpeta indicada
* El comando "?" preguntará a tu bot cuántos archivos tiene en cola
* El comando "quit" para el bot
