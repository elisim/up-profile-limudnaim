from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from config import config
import sys
from time import sleep


url = config["profile_url"]
mail = config["email"]
password = config["password"]

log_file = "log.txt"
debug_flag = False

def log_to_file(log):
	# append current time to log messege
	now = datetime.now().strftime("%D %H:%M") 
	log = f"{log} Time: {now}\n"

	if debug_flag:
		print(log)
	else:
		with open(log_file, "a") as logto:
			logto.write(log)

def main():
	global debug_flag
	debug_flag = '-d' in sys.argv
	options = webdriver.ChromeOptions()
	if not debug_flag:
		options.add_argument('headless')
		options.add_argument('--no-sandbox')
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(options=options)
	try:
		driver.get(url)

		try: # not always presented
			driver.find_element_by_id("limudnaim-nav-bar-burger").click() # NEW: open menu (if exist)
			sleep(2)
		except:
			pass
			
		driver.find_element_by_class_name("icon-login").click() # login to your account
		driver.find_element_by_id("edit-name").send_keys(mail) # fill email input
		driver.find_element_by_id("edit-pass").send_keys(password) # fill password input
		driver.find_element_by_id("edit-submit").submit() # submit

		try: # no always pop up
			driver.find_element_by_class_name("modal-close").click()
		except:
			pass

		up_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "update-profile")))
		# class will contain "update-disable" if up is disabled now
		if up_button.get_attribute("class") == "update-profile": 
			sleep(2)
			up_button.click() # up my profile
			up_success = True
		else:
			time_to_up = up_button.text.split()[-1]
			up_success = False 
			
		if up_success:
			log_to_file("profile update SUCCESS!")
		else:
			log_to_file(f"profile update FAILED! You can update at {time_to_up}.")
	except:
		log_to_file("Error! Exiting...")
		raise
	finally:
		driver.close()

if __name__ == "__main__":
	main()