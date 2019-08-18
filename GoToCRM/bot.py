import uuid
import telebot
import os
# TODO: указать имя сайта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GoToCRM.settings")
import django
django.setup()

from crm.models import Student

telebot.apihelper.proxy = {''}

# TODO: указать token
token = "858742418:AAENpIdsVPlMhb_wiZVktIWHtV-OzJ4JIN0"
bot = telebot.TeleBot(token=token)

data = {}

@bot.message_handler(content_types=['text'])
def search(message):
    text = message.text
    user = message.chat.id
    try:
        name, surname = text.split(' ')
    except:
        bot.send_message(user, "Пришлите имя и фамилию")
        return

    student = Student.objects.filter(name=name, surname=surname).first()
    if student:
        data[user] = student
        bot.send_message(user, "Присылайте фото...")
    else:
        bot.send_message(user, "Я не нашел...")

@bot.message_handler(content_types=['photo'])
def photo(message):
    user = message.chat.id

    if user not in data:
        bot.send_message(user, "Сначала пришлите имя")
        return

    # скачивание файла
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    downloaded_file = bot.download_file(path.file_path)

    # узнаем расширение и случайное придумываем имя
    extn = '.' + str(path.file_path).split('.')[-1]
    name = 'avatars/' + str(uuid.uuid4()) + extn

    # создаем файл и записываем туда данные
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    student = data[user]

    student.photo = name
    student.save()
    bot.send_message(message.chat.id, 'ok')

bot.polling(none_stop=True)