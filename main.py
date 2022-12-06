from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyautogui

service = Service(executable_path="/path/to/chromedriver")
driver = webdriver.Chrome(service=service)
# to maximize the browser window
driver.maximize_window()
#get method to launch the URL
driver.get("https://sec.report/Document/0000070858-20-000061/bac-20200923.htm")
actionChains = ActionChains(driver)
actionChains.key_down(Keys.LEFT_CONTROL).send_keys(str('\u0055')).perform()
# action.perform()

# pyautogui.keyDown('ctrl')
# pyautogui.keyDown('f')
# pyautogui.keyUp('ctrl')
# pyautogui.keyUp('f')
# pyautogui.hotkey('ctrl','f', interval=0.25)
# perform the ctrl+f pressing action
# pyautogui.typewrite('Your keyword')    
# pyautogui.hotkey('Return')
sleep(10)
#to close the browser
driver.close()



# url = driver.get('')
# rowcount = driver.findElements(By.xpath("\\a[contains(@id,'edit')]")).size()