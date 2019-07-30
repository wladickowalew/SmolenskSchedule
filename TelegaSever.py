import telebot
from raspisanie import RaspParser as Rasp

bot = telebot.TeleBot('741975871:AAEro-_Ky0DRfs6-rWplI5UwcQLk79_nXZQ')
rasp = Rasp("смоленск")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, Я автобусный бот в Смоленске! Пока я умею делать только следующее:')
    help_message(message)

@bot.message_handler(commands=['help'])
def help_message(message):
	commands = {"/help": " - поможет вам рассказать, что я умею",
				"/work_days":" - расписание вашего автобуса по рабочим дням",
				"/week_end":" - расписание вашего автобуса по выходным дням",
				"/all_days":" - полное расписание вашего автобуса"}
	answer = "\n".join([command + description for command, description in commands.items()])
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['work_days'])
def work_days_message(message):
	print(message.text)
	num = message.text.split()
	if (len(num) == 1):
		num = "3"
	answer = rasp.get_work_day_t(num[1])
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['week_end'])
def week_end_message(message):
	num = message.text.split()
	if (len(num) == 1):
		num = "3"
	answer = rasp.get_week_end_t(num[1])
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['all_days'])
def all_day_message(message):
	work_days_message(message)
	week_end_message(message)

bot.polling()