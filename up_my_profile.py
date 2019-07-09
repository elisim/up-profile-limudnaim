from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from config import config


url = config["profile_url"]
mail = config["email"]
password = config["password"]

log_file = "log.txt"

def log_to_file(log):
	with open(log_file, "a") as logto:
		logto.write(log)

def main():
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	# options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	driver.find_element_by_class_name("login").click() # login to your account 
	driver.find_element_by_id("edit-name").send_keys(mail) # fill email input
	driver.find_element_by_id("edit-pass").send_keys(password) # fill password input
	driver.find_element_by_id("edit-submit").submit() # submit
	driver.find_element_by_class_name("modal-close").click()
	up_button = driver.find_element_by_class_name("update-profile")

	# class will contain "update-disable" if up is disabled now
	if up_button.get_attribute("class") == "update-profile": 
		up_button.click() # up my profile
		up_success = True
	else:
		time_to_up = up_button.text.split()[-1]
		up_success = False 
		
	now = datetime.now().strftime("%D %H:%M") 
	if up_success:
		log_to_file(f"profile update SUCCESS! Time: {now}\n" )
	else:
		log_to_file(f"profile update FAILED! You can update at {time_to_up}. Time: {now}.\n")

	driver.close()

if __name__ == "__main__":
	main()