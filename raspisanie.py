import SmolenskParse

#example data for tests
city = "Смоленск"
number = "53"
#example data for tests

CityParser = None


class RaspParser():

	def __init__(self, city):
		Cities = {"смоленск": SmolenskParse}
		self.city = city 
		if city.strip().lower() in Cities.keys():
			self.CityParser = Cities[city.lower()]
		else:
			print("К сожалению на данный момент наш сервис не поддерживает ваш город")
			return

	def print_ans(self, ans, is_free):
		print('--------------------------------------------------------------------')
		if type(ans) is str:
			print(ans)
		else:
			if is_free:
				print("По выходным дням:")
			else:
				print("По рабочим дням:")
			print("\n\n".join([(k + "\n" + " ".join(v)) for k, v in ans.items()]))
		print('--------------------------------------------------------------------\n\n')

	def create_ans_for_telega(self, dict, is_free):
		if type(dict) is str:
			print(dict)
		else:
			if is_free:
				ans = "По выходным дням:\n"
			else:
				ans = "По рабочим дням:\n"
			ans += "\n\n".join([(k + "\n" + " ".join(v)) for k, v in dict.items()])
		return ans

	def get_work_day(self, number):
		return self.CityParser.get_work_day_rasp(number)

	def get_week_end(self, number):
		return self.CityParser.get_free_day_rasp(number)

	def get_work_day_t(self, number):
		ans = self.get_work_day(number)
		return self.create_ans_for_telega(ans, False)

	def get_week_end_t(self, number):
		ans =  self.get_week_end(number)
		return self.create_ans_for_telega(ans, True)

if __name__ == "__main__":
	rasp = RaspParser("смоленск")
	rasp.print_ans(rasp.get_work_day("19"), False)
	rasp.print_ans(rasp.get_week_end("19"), True)
	print(rasp.get_week_end_t("3"))