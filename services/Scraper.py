from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import os

class Scraper:
	def __init__(self):
		self.driver = webdriver.Chrome()

	def downloadStats(self, name):
		# Navigate to nba search page
		self.driver.get("http://www.nba.com/search/?text=%s" % name.replace(' ', '+'))

		# Click on player search head
		player_page_link = self.driver.find_element_by_css_selector('.nbaPlayerSearchHead a')
		name = player_page_link.text.split("-")[0].strip()
		print("Downloading stats for %s..." % name)
		player_page_link.click()

		# Navigate to logs link
		player_logs_link = self.driver.find_element_by_css_selector('#tab-logs')
		url = player_logs_link.get_attribute('href')
		self.driver.get(url)


		# Find rows in table
		rows = self.driver.find_elements_by_css_selector('table tr')

		# Create header and data rows
		headers = ['Player']
		data = []

		# Loop through each row
		for rr, row in enumerate(rows):

			# If header row
			if rr == 0:
				cols = row.find_elements_by_css_selector('th')
				for col in cols:
					headers.append(col.text.encode("ascii"))

			# If data rows
			else:
				cols = row.find_elements_by_css_selector('td')
				data_line = [name.encode("ascii")]
				for col in cols:
					data_line.append(col.text.encode("ascii"))
				data.append(data_line)

		# Write data to csv file
		f = open("data/%s.csv" % name, "wb")
		writer = csv.writer(f)
		writer.writerow(headers)
		for datum in data:
			writer.writerow(datum)
		f.close()

	def quit(self):
		self.driver.quit()