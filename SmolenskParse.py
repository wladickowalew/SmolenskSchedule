from bs4 import BeautifulSoup
import urllib.request

URL = "http://ak1308.ru/rasp/"

#Расписание на будние дни
WAY_WORK = {"1":"2-1", "2":"3-2", "3":"4-3", "7":"5-7", "8":"6-8", "9":"7-9", "10":"8-10", 
		"11":"9-11", "12":"10-12", "14":"11-14", "15":"12-15", "17":"13-17", "19":"14-19",
		"22":"15-22", "23":"16-23", "24":"17-24", "25":"18-25", "28":"20-28", "30":"21-30",
		"31":"22-31k", "33":"23-33", "34":"24-34","49":"26-49", "50":"27-50", "53":"151-53",
		"54":"161-54r", "105":"109-105", "106":"63-106", "108":"65-108", "118":"200-118",
		"127":"72-127", "141":"114-141", "147":"158-147r", "164":"81-164"}

#Расписание на выходные дни
WAY_FREE = {"1":"30-1v", "2":"31-2v", "3":"32-3v", "7":"33-7v", "8":"34-8v", "9":"35-9v", 
		"10":"36-10v", "11":"37-11v","12":"38-12v","14":"56-14v", "15":"39-15v", "17":"40-17v",
		"19":"41-19v","22":"42-22v", "24":"43-24v", "25":"44-25v", "28":"46-28v","30":"47-30v",
		"31":"48-31v", "33":"49-33v", "34":"50-34v","49":"52-49v","50":"53-50v","53":"152-53v",
		"54":"162-54v","105":"115-105v", "106":"84-106v", "108":"86-108v","118":"201-118v",
		"127":"93-127v","141":"120-141v", "147":"159-147v","164":"101-164v"}

#Типы маршрутов
TYPE  = {"dachnue/":["105","118","141","147"],
		"rabdnipr/":["106","108","127", "164"],
		"rabdni/":["1", "2", "3", "7", "8", "9", "10", "11", "12", "14", "15",
			"17", "19", "22", "23", "24", "25","28","30","31","33","34","49","50","53","54"]}

def get_work_day_rasp(number):
	answer = {}
	res = get_rasp(number, WAY_WORK)
	if res == "Error":
		return "К сожалению нет расписания для вашего автобуса на рабочие дни"
	for k, v in res.items():
		answer["от остановки \"" + k + "\":"] = v
	return answer

def get_free_day_rasp(number):
	answer = {}
	res = get_rasp(number, WAY_FREE)
	if res == "Error":
		return "К сожалению нет расписания для вашего автобуса на выходные дни"
	for k, v in res.items():
		answer["от остановки \"" + k + "\":"] = v
	return answer

def get_rasp(number, days):
	for key in TYPE:
		if number in TYPE[key]:
			this_type = key
			break
	else:
		return "Error"
	if number not in days.keys():
		return "Error"
	url = URL + this_type + days[number]
	html_doc = get_html(url)
	rasp = parse_block(html_doc)
	return rasp

def get_html(url):
	response = urllib.request.urlopen(url)
	return response.read().decode('utf-8', 'ignore')

def parse_block(html):
	soup = BeautifulSoup(html, "html.parser")
	block = soup.find("div", class_="article-content")
	row = block.find("p", mce_style="text-align: center;")
	tag_list = list(map(str, list(row)))
	answer = parse_rasp(tag_list)
	return answer

def parse_rasp(tag_array):
	answer = {}
	counter = 0
	current_string = tag_array[counter]
	while not current_string.startswith('='):
		counter += 1
		current_string = tag_array[counter]

	val_list = []
	key = current_string.replace("=","").strip()
	counter += 1
	current_string = tag_array[counter]
	while not current_string.startswith('='):
		if current_string != "<br/>":
			val_list.extend(current_string.split())
		counter += 1
		current_string = tag_array[counter]
	answer[key] = val_list

	val_list = []
	key = current_string.replace("=","").strip()
	counter += 1
	tag_array = tag_array[counter:]
	for current_string in tag_array:
		if current_string != "<br/>":
			val_list.extend(current_string.split())
	answer[key] = val_list
	return answer
