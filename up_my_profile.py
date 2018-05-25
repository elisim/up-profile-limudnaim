from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from config import config


url = config["profile_url"]
mail = config["email"]
password = config["password"]


def main():
	driver = webdriver.Chrome()	
	driver.get(url)

	driver.find_element_by_class_name("login").click() # login to your account 
	driver.find_element_by_id("edit-name").send_keys(mail) # fill email input
	driver.find_element_by_id("edit-pass").send_keys(password) # fill password input
	driver.find_element_by_id("edit-submit").submit() # submit

	up_button = driver.find_element_by_class_name("update-profile")

	# class will contain "update-disable" if up is disabled now
	if up_button.get_attribute("class") == "update-profile": 
		up_button.click() # up my profile!!!
		up_success = True
		time = datetime.now().strftime("%H:%M") 
	else:
		up_success = False 
		time = up_button.text.split()[-1]

	if up_success:
		print "profile update SUCCESS! Time: " + time	
	else:
		print "profile update FAILED! You can update at " + time

	driver.close()

if __name__ == "__main__":
	main()